"""Job description normalization service."""

import re
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from bs4 import BeautifulSoup
import logging

from app.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class NormalizedJobDescription:
    """Normalized job description structure."""
    
    title: str
    company: str
    location: Optional[str] = None
    description: str
    requirements: List[str]
    responsibilities: List[str]
    qualifications: List[str]
    benefits: List[str]
    salary_range: Optional[str] = None
    employment_type: Optional[str] = None
    experience_level: Optional[str] = None
    skills: List[str]
    education: Optional[str] = None
    industry: Optional[str] = None
    department: Optional[str] = None
    raw_content: str = ""


class JobDescriptionNormalizer:
    """Service for normalizing job descriptions."""
    
    def __init__(self):
        self.requirement_patterns = [
            r'(?:requirements?|qualifications?|must have|should have|need to have):\s*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'(?:minimum|required|preferred)\s+(?:qualifications?|requirements?|experience):\s*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'(?:experience|skills?|knowledge)\s+(?:required|needed|preferred):\s*(.*?)(?=\n\n|\n[A-Z]|$)',
        ]
        
        self.responsibility_patterns = [
            r'(?:responsibilities?|duties?|what you\'ll do|key responsibilities?):\s*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'(?:role|position|job)\s+(?:responsibilities?|duties?):\s*(.*?)(?=\n\n|\n[A-Z]|$)',
        ]
        
        self.benefit_patterns = [
            r'(?:benefits?|perks?|what we offer|compensation):\s*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'(?:health|dental|vision|insurance|401k|pto|vacation):\s*(.*?)(?=\n\n|\n[A-Z]|$)',
        ]
        
        self.salary_patterns = [
            r'\$[\d,]+(?:\s*-\s*\$[\d,]+)?(?:\s*(?:per\s+)?(?:year|month|hour|annually|monthly|hourly))?',
            r'(?:salary|compensation|pay)\s*(?:range|package)?\s*:\s*\$[\d,]+(?:\s*-\s*\$[\d,]+)?',
            r'(?:competitive|attractive|excellent)\s+(?:salary|compensation|pay)',
        ]
        
        self.employment_type_patterns = [
            r'(?:full\s*-?\s*time|part\s*-?\s*time|contract|temporary|permanent|remote|hybrid|on\s*-?\s*site)',
            r'(?:employment\s+type|job\s+type|work\s+arrangement):\s*(.*?)(?=\n|$)',
        ]
        
        self.experience_level_patterns = [
            r'(?:entry\s*-?\s*level|junior|mid\s*-?\s*level|senior|lead|principal|executive)',
            r'(?:experience\s+level|seniority):\s*(.*?)(?=\n|$)',
        ]
    
    def normalize(self, raw_content: Dict[str, Any]) -> NormalizedJobDescription:
        """
        Normalize raw scraped content into structured job description.
        
        Args:
            raw_content: Raw scraped content from web scraping
            
        Returns:
            Normalized job description
        """
        try:
            # Extract basic fields
            title = self._clean_text(raw_content.get('title', ''))
            company = self._clean_text(raw_content.get('company', ''))
            location = self._clean_text(raw_content.get('location', ''))
            
            # Get description content
            description_html = raw_content.get('description', '')
            description_text = self._html_to_text(description_html)
            
            # If no description from scraping, use full content
            if not description_text:
                description_text = self._html_to_text(raw_content.get('content', ''))
            
            # Extract structured sections
            requirements = self._extract_requirements(description_text)
            responsibilities = self._extract_responsibilities(description_text)
            benefits = self._extract_benefits(description_text)
            salary_range = self._extract_salary_range(description_text)
            employment_type = self._extract_employment_type(description_text)
            experience_level = self._extract_experience_level(description_text)
            skills = self._extract_skills(description_text)
            education = self._extract_education(description_text)
            industry = self._extract_industry(description_text)
            department = self._extract_department(description_text)
            
            # Create normalized structure
            normalized = NormalizedJobDescription(
                title=title,
                company=company,
                location=location,
                description=description_text,
                requirements=requirements,
                responsibilities=responsibilities,
                benefits=benefits,
                salary_range=salary_range,
                employment_type=employment_type,
                experience_level=experience_level,
                skills=skills,
                education=education,
                industry=industry,
                department=department,
                raw_content=json.dumps(raw_content)
            )
            
            return normalized
            
        except Exception as e:
            logger.error(f"Failed to normalize job description: {str(e)}")
            # Return minimal structure on error
            return NormalizedJobDescription(
                title=raw_content.get('title', ''),
                company=raw_content.get('company', ''),
                description=raw_content.get('description', ''),
                requirements=[],
                responsibilities=[],
                benefits=[],
                skills=[]
            )
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # Remove common unwanted characters
        text = re.sub(r'[\u200b\u200c\u200d\u200e\u200f]', '', text)
        
        return text
    
    def _html_to_text(self, html_content: str) -> str:
        """Convert HTML content to clean text."""
        if not html_content:
            return ""
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text and clean it
            text = soup.get_text()
            text = self._clean_text(text)
            
            return text
            
        except Exception as e:
            logger.warning(f"Failed to parse HTML: {str(e)}")
            return html_content
    
    def _extract_requirements(self, text: str) -> List[str]:
        """Extract requirements from text."""
        requirements = []
        
        # Try pattern matching
        for pattern in self.requirement_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                requirements.extend(self._split_bullet_points(match))
        
        # If no pattern matches, try to find bullet points with requirement-like content
        if not requirements:
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if line and any(keyword in line.lower() for keyword in ['years', 'experience', 'degree', 'certification', 'proficiency']):
                    requirements.append(line)
        
        return list(set(requirements))  # Remove duplicates
    
    def _extract_responsibilities(self, text: str) -> List[str]:
        """Extract responsibilities from text."""
        responsibilities = []
        
        for pattern in self.responsibility_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                responsibilities.extend(self._split_bullet_points(match))
        
        return list(set(responsibilities))
    
    def _extract_benefits(self, text: str) -> List[str]:
        """Extract benefits from text."""
        benefits = []
        
        for pattern in self.benefit_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                benefits.extend(self._split_bullet_points(match))
        
        return list(set(benefits))
    
    def _extract_salary_range(self, text: str) -> Optional[str]:
        """Extract salary range from text."""
        for pattern in self.salary_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0]
        return None
    
    def _extract_employment_type(self, text: str) -> Optional[str]:
        """Extract employment type from text."""
        for pattern in self.employment_type_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0]
        return None
    
    def _extract_experience_level(self, text: str) -> Optional[str]:
        """Extract experience level from text."""
        for pattern in self.experience_level_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0]
        return None
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from text."""
        skills = []
        
        # Common skill keywords
        skill_keywords = [
            'python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
            'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git',
            'sql', 'mongodb', 'redis', 'elasticsearch', 'kafka', 'rabbitmq',
            'machine learning', 'ai', 'data science', 'analytics', 'statistics',
            'agile', 'scrum', 'kanban', 'jira', 'confluence', 'slack',
            'excel', 'powerpoint', 'word', 'photoshop', 'illustrator',
            'salesforce', 'hubspot', 'marketo', 'google analytics'
        ]
        
        text_lower = text.lower()
        for skill in skill_keywords:
            if skill in text_lower:
                skills.append(skill)
        
        return list(set(skills))
    
    def _extract_education(self, text: str) -> Optional[str]:
        """Extract education requirements from text."""
        education_patterns = [
            r'(?:bachelor\'s|master\'s|phd|degree|diploma|certification)\s+(?:in|of)?\s+([^.\n]+)',
            r'(?:education|degree|qualification):\s*([^.\n]+)',
        ]
        
        for pattern in education_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0].strip()
        
        return None
    
    def _extract_industry(self, text: str) -> Optional[str]:
        """Extract industry from text."""
        industry_patterns = [
            r'(?:industry|sector):\s*([^.\n]+)',
            r'(?:technology|healthcare|finance|education|retail|manufacturing|consulting)',
        ]
        
        for pattern in industry_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0].strip()
        
        return None
    
    def _extract_department(self, text: str) -> Optional[str]:
        """Extract department from text."""
        department_patterns = [
            r'(?:department|team|division):\s*([^.\n]+)',
            r'(?:engineering|marketing|sales|hr|finance|operations|product|design)',
        ]
        
        for pattern in department_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0].strip()
        
        return None
    
    def _split_bullet_points(self, text: str) -> List[str]:
        """Split text into bullet points or sentences."""
        # Split by bullet points
        bullet_points = re.split(r'[•·▪▫‣⁃]\s*', text)
        if len(bullet_points) > 1:
            return [point.strip() for point in bullet_points if point.strip()]
        
        # Split by numbered lists
        numbered_points = re.split(r'\d+\.\s*', text)
        if len(numbered_points) > 1:
            return [point.strip() for point in numbered_points if point.strip()]
        
        # Split by line breaks
        lines = text.split('\n')
        return [line.strip() for line in lines if line.strip()]


def normalize_job_description(raw_content: Dict[str, Any]) -> NormalizedJobDescription:
    """
    Convenience function to normalize job description.
    
    Args:
        raw_content: Raw scraped content from web scraping
        
    Returns:
        Normalized job description
    """
    normalizer = JobDescriptionNormalizer()
    return normalizer.normalize(raw_content)
