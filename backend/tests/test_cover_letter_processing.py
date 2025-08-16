"""Tests for cover letter processing functionality."""

import pytest
from unittest.mock import Mock, patch
from typing import Dict, Any

from app.services.cover_letter_processing import CoverLetterGenerator, CoverLetterDocumentGenerator


class TestCoverLetterGenerator:
    """Test cover letter generation functionality."""
    
    @patch('app.services.cover_letter_processing.settings')
    @patch('app.services.cover_letter_processing.OpenAI')
    def test_llm_client_setup(self, mock_openai, mock_settings):
        """Test LLM client setup."""
        mock_settings.LLM_PROVIDER = "openai"
        mock_settings.OPENAI_API_KEY = "test-key"
        
        generator = CoverLetterGenerator()
        
        assert generator.client is not None
        mock_openai.assert_called_once_with(api_key="test-key")
    
    @patch('app.services.cover_letter_processing.settings')
    def test_llm_client_setup_missing_key(self, mock_settings):
        """Test LLM client setup with missing API key."""
        mock_settings.LLM_PROVIDER = "openai"
        mock_settings.OPENAI_API_KEY = None
        
        with pytest.raises(ValueError, match="OpenAI API key not configured"):
            CoverLetterGenerator()
    
    @patch('app.services.cover_letter_processing.settings')
    def test_llm_client_setup_unsupported_provider(self, mock_settings):
        """Test LLM client setup with unsupported provider."""
        mock_settings.LLM_PROVIDER = "unsupported"
        
        with pytest.raises(NotImplementedError, match="LLM provider unsupported not implemented"):
            CoverLetterGenerator()
    
    def test_build_cover_letter_prompt(self):
        """Test cover letter prompt building."""
        generator = CoverLetterGenerator()
        
        job_description = {
            "title": "Software Engineer",
            "company": "Test Corp",
            "summary": "We are looking for a talented engineer",
            "requirements": ["Python", "FastAPI", "PostgreSQL"]
        }
        
        resume_data = {
            "experience": [
                {"title": "Software Engineer", "company": "Previous Corp", "duration": "2 years"}
            ],
            "skills": ["Python", "FastAPI", "PostgreSQL"],
            "education": [{"degree": "BS Computer Science", "institution": "University"}]
        }
        
        personal_info = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "(555) 123-4567"
        }
        
        prompt = generator._build_cover_letter_prompt(job_description, resume_data, personal_info)
        
        assert "Software Engineer" in prompt
        assert "Test Corp" in prompt
        assert "John Doe" in prompt
        assert "Python" in prompt
        assert "JSON" in prompt
    
    def test_parse_cover_letter_content_json(self):
        """Test parsing cover letter content from JSON response."""
        generator = CoverLetterGenerator()
        
        content = '''
        {
            "greeting": "Dear Hiring Manager,",
            "opening": "I am excited to apply for the Software Engineer position",
            "body": "With my experience in Python and FastAPI...",
            "closing": "I look forward to discussing this opportunity",
            "signature": "Sincerely,\\nJohn Doe"
        }
        '''
        
        personal_info = {"name": "John Doe"}
        
        result = generator._parse_cover_letter_content(content, personal_info)
        
        assert result["greeting"] == "Dear Hiring Manager,"
        assert result["opening"] == "I am excited to apply for the Software Engineer position"
        assert result["body"] == "With my experience in Python and FastAPI..."
        assert result["closing"] == "I look forward to discussing this opportunity"
        assert result["signature"] == "Sincerely,\nJohn Doe"
    
    def test_parse_cover_letter_content_fallback(self):
        """Test parsing cover letter content with fallback to plain text."""
        generator = CoverLetterGenerator()
        
        content = '''
        Dear Hiring Manager,
        
        I am excited to apply for the Software Engineer position.
        
        With my experience in Python and FastAPI, I believe I would be a great fit.
        
        I look forward to discussing this opportunity.
        '''
        
        personal_info = {"name": "John Doe"}
        
        result = generator._parse_cover_letter_content(content, personal_info)
        
        assert result["greeting"] == "Dear Hiring Manager,"
        assert "Software Engineer" in result["opening"]
        assert "Python" in result["body"]
        assert result["signature"] == "Sincerely,\nJohn Doe"


class TestCoverLetterDocumentGenerator:
    """Test cover letter document generation functionality."""
    
    @patch('app.templates.default_cover_letter_template.get_template')
    def test_document_generator_init(self, mock_get_template):
        """Test document generator initialization."""
        mock_template = {"css": "test-css"}
        mock_get_template.return_value = mock_template
        
        generator = CoverLetterDocumentGenerator()
        
        assert generator.template == mock_template
        mock_get_template.assert_called_once()
    
    @patch('app.templates.default_cover_letter_template.get_template')
    def test_generate_html(self, mock_get_template):
        """Test HTML generation for PDF conversion."""
        mock_template = {"css": "test-css"}
        mock_get_template.return_value = mock_template
        
        generator = CoverLetterDocumentGenerator()
        
        cover_letter_content = {
            "greeting": "Dear Hiring Manager,",
            "opening": "I am excited to apply",
            "body": "With my experience",
            "closing": "I look forward to discussing",
            "signature": "Sincerely,\nJohn Doe"
        }
        
        job_description = {"company": "Test Corp"}
        personal_info = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "(555) 123-4567",
            "location": "San Francisco, CA"
        }
        
        html = generator._generate_html(cover_letter_content, job_description, personal_info)
        
        assert "John Doe" in html
        assert "Test Corp" in html
        assert "Dear Hiring Manager," in html
        assert "john@example.com" in html
        assert "San Francisco, CA" in html


class TestCoverLetterTasks:
    """Test cover letter Celery tasks."""
    
    @patch('app.services.cover_letter_processing.CoverLetterGenerator')
    @patch('app.services.cover_letter_processing.CoverLetterDocumentGenerator')
    @patch('app.services.cover_letter_processing.file_storage')
    def test_generate_cover_letter_task(self, mock_file_storage, mock_doc_generator, mock_generator_class):
        """Test cover letter generation task."""
        from app.services.cover_letter_processing import generate_cover_letter
        
        # Mock the generator
        mock_generator = Mock()
        mock_generator_class.return_value = mock_generator
        mock_generator.generate_cover_letter_content.return_value = {
            "greeting": "Dear Hiring Manager,",
            "opening": "I am excited to apply",
            "body": "With my experience",
            "closing": "I look forward to discussing",
            "signature": "Sincerely,\nJohn Doe"
        }
        
        # Mock the document generator
        mock_doc_gen = Mock()
        mock_doc_generator.return_value = mock_doc_gen
        mock_doc_gen.generate_docx.return_value = b"docx-content"
        mock_doc_gen.generate_pdf.return_value = b"pdf-content"
        
        # Mock file storage
        mock_file_storage.upload_file.return_value = "https://example.com/file"
        
        # Create a mock task
        mock_task = Mock()
        mock_task.request.id = "test-task-id"
        
        # Call the task
        result = generate_cover_letter(mock_task, 1, 1, 1)
        
        # Verify the result
        assert result["application_id"] == 1
        assert result["job_id"] == 1
        assert result["resume_id"] == 1
        assert result["status"] == "generated"
        assert "docx_url" in result
        assert "pdf_url" in result
        assert "cover_letter_content" in result
    
    @patch('app.services.cover_letter_processing.CoverLetterGenerator')
    def test_preview_cover_letter_task(self, mock_generator_class):
        """Test cover letter preview task."""
        from app.services.cover_letter_processing import preview_cover_letter
        
        # Mock the generator
        mock_generator = Mock()
        mock_generator_class.return_value = mock_generator
        mock_generator.generate_cover_letter_content.return_value = {
            "greeting": "Dear Hiring Manager,",
            "opening": "I am excited to apply",
            "body": "With my experience",
            "closing": "I look forward to discussing",
            "signature": "Sincerely,\nJohn Doe"
        }
        
        # Create a mock task
        mock_task = Mock()
        mock_task.request.id = "test-task-id"
        
        # Test data
        job_description = {"title": "Software Engineer", "company": "Test Corp"}
        resume_data = {"experience": [], "skills": []}
        personal_info = {"name": "John Doe"}
        
        # Call the task
        result = preview_cover_letter(mock_task, job_description, resume_data, personal_info)
        
        # Verify the result
        assert result["status"] == "preview_generated"
        assert "cover_letter_content" in result
        assert result["cover_letter_content"]["greeting"] == "Dear Hiring Manager,"


if __name__ == "__main__":
    pytest.main([__file__])
