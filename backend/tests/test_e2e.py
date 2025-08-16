"""End-to-end tests for complete workflow."""

import pytest
import time
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import get_db, Base

# Create in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestCompleteWorkflow:
    """Test the complete workflow from job extraction to application creation."""
    
    def test_complete_workflow(self):
        """Test the complete workflow end-to-end."""
        # Step 1: Extract job description
        job_url = "https://example.com/software-engineer-job"
        job_response = client.post("/api/v1/jobs/extract", json={"url": job_url})
        assert job_response.status_code == 200
        job_data = job_response.json()
        job_id = job_data["id"]
        
        print(f"✅ Job extracted with ID: {job_id}")
        
        # Step 2: Upload resume
        resume_content = b"fake resume content"
        files = {"file": ("test_resume.pdf", resume_content, "application/pdf")}
        resume_response = client.post("/api/v1/resumes/upload", files=files)
        assert resume_response.status_code == 200
        resume_data = resume_response.json()
        resume_id = resume_data["id"]
        
        print(f"✅ Resume uploaded with ID: {resume_id}")
        
        # Step 3: Create application
        app_response = client.post("/api/v1/applications", json={
            "job_id": job_id,
            "resume_id": resume_id
        })
        assert app_response.status_code == 200
        app_data = app_response.json()
        app_id = app_data["id"]
        
        print(f"✅ Application created with ID: {app_id}")
        
        # Step 4: Check application status
        status_response = client.get(f"/api/v1/applications/{app_id}/status")
        assert status_response.status_code == 200
        status_data = status_response.json()
        assert status_data["id"] == app_id
        
        print(f"✅ Application status checked: {status_data['status']}")
        
        # Step 5: Get job details
        job_details_response = client.get(f"/api/v1/jobs/{job_id}")
        assert job_details_response.status_code == 200
        job_details = job_details_response.json()
        assert job_details["id"] == job_id
        
        print(f"✅ Job details retrieved: {job_details['title']}")
        
        # Step 6: Get resume details
        resume_details_response = client.get(f"/api/v1/resumes/{resume_id}")
        assert resume_details_response.status_code == 200
        resume_details = resume_details_response.json()
        assert resume_details["id"] == resume_id
        
        print(f"✅ Resume details retrieved: {resume_details['filename']}")
        
        print("🎉 Complete workflow test passed!")


class TestErrorHandling:
    """Test error handling scenarios."""
    
    def test_invalid_job_url(self):
        """Test handling of invalid job URLs."""
        response = client.post("/api/v1/jobs/extract", json={"url": "not-a-url"})
        assert response.status_code == 422  # Validation error
        
        print("✅ Invalid URL handling works correctly")
    
    def test_invalid_file_type(self):
        """Test handling of invalid file types."""
        files = {"file": ("test.txt", b"text content", "text/plain")}
        response = client.post("/api/v1/resumes/upload", files=files)
        assert response.status_code == 400  # Bad request
        
        print("✅ Invalid file type handling works correctly")
    
    def test_nonexistent_job(self):
        """Test handling of nonexistent job ID."""
        response = client.get("/api/v1/jobs/99999")
        assert response.status_code == 404  # Not found
        
        print("✅ Nonexistent job handling works correctly")
    
    def test_nonexistent_resume(self):
        """Test handling of nonexistent resume ID."""
        response = client.get("/api/v1/resumes/99999")
        assert response.status_code == 404  # Not found
        
        print("✅ Nonexistent resume handling works correctly")
    
    def test_nonexistent_application(self):
        """Test handling of nonexistent application ID."""
        response = client.get("/api/v1/applications/99999")
        assert response.status_code == 404  # Not found
        
        print("✅ Nonexistent application handling works correctly")


class TestAPICompatibility:
    """Test API compatibility with frontend expectations."""
    
    def test_job_response_format(self):
        """Test that job response format matches frontend expectations."""
        response = client.post("/api/v1/jobs/extract", json={"url": "https://example.com/test"})
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        required_fields = ["id", "title", "company", "location", "description", "requirements", "created_at"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        print("✅ Job response format is compatible with frontend")
    
    def test_resume_response_format(self):
        """Test that resume response format matches frontend expectations."""
        files = {"file": ("test.pdf", b"content", "application/pdf")}
        response = client.post("/api/v1/resumes/upload", files=files)
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        required_fields = ["id", "filename", "created_at"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        print("✅ Resume response format is compatible with frontend")
    
    def test_application_response_format(self):
        """Test that application response format matches frontend expectations."""
        # First create job and resume
        job_response = client.post("/api/v1/jobs/extract", json={"url": "https://example.com/test"})
        job_id = job_response.json()["id"]
        
        files = {"file": ("test.pdf", b"content", "application/pdf")}
        resume_response = client.post("/api/v1/resumes/upload", files=files)
        resume_id = resume_response.json()["id"]
        
        # Create application
        response = client.post("/api/v1/applications", json={
            "job_id": job_id,
            "resume_id": resume_id
        })
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        required_fields = ["id", "job_id", "resume_id", "status", "created_at"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        print("✅ Application response format is compatible with frontend")


if __name__ == "__main__":
    print("🚀 Starting end-to-end tests...")
    
    # Run tests
    test_workflow = TestCompleteWorkflow()
    test_workflow.test_complete_workflow()
    
    test_errors = TestErrorHandling()
    test_errors.test_invalid_job_url()
    test_errors.test_invalid_file_type()
    test_errors.test_nonexistent_job()
    test_errors.test_nonexistent_resume()
    test_errors.test_nonexistent_application()
    
    test_compatibility = TestAPICompatibility()
    test_compatibility.test_job_response_format()
    test_compatibility.test_resume_response_format()
    test_compatibility.test_application_response_format()
    
    print("🎉 All end-to-end tests completed successfully!")
