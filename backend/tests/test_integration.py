"""Integration tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import get_db, Base
from app.models import Job, Resume, JobApplication

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


class TestJobEndpoints:
    """Test job-related endpoints."""
    
    def test_extract_job_description(self):
        """Test job description extraction endpoint."""
        url = "https://example.com/job-posting"
        response = client.post("/api/v1/jobs/extract", json={"url": url})
        
        assert response.status_code == 200
        data = response.json()
        assert data["url"] == url
        assert data["status"] == "pending"
        assert "id" in data
    
    def test_get_job_description(self):
        """Test getting job description by ID."""
        # First create a job
        url = "https://example.com/job-posting-2"
        create_response = client.post("/api/v1/jobs/extract", json={"url": url})
        job_id = create_response.json()["id"]
        
        # Then get it
        response = client.get(f"/api/v1/jobs/{job_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == job_id
        assert data["url"] == url
    
    def test_get_job_status(self):
        """Test getting job processing status."""
        # First create a job
        url = "https://example.com/job-posting-3"
        create_response = client.post("/api/v1/jobs/extract", json={"url": url})
        job_id = create_response.json()["id"]
        
        # Then get status
        response = client.get(f"/api/v1/jobs/{job_id}/status")
        assert response.status_code == 200
        data = response.json()
        assert data["job_id"] == job_id
        assert "status" in data


class TestResumeEndpoints:
    """Test resume-related endpoints."""
    
    def test_upload_resume(self):
        """Test resume upload endpoint."""
        # Create a mock PDF file
        files = {"file": ("test.pdf", b"fake pdf content", "application/pdf")}
        response = client.post("/api/v1/resumes/upload", files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "test.pdf"
        assert "id" in data
    
    def test_get_resume(self):
        """Test getting resume by ID."""
        # First upload a resume
        files = {"file": ("test2.pdf", b"fake pdf content 2", "application/pdf")}
        upload_response = client.post("/api/v1/resumes/upload", files=files)
        resume_id = upload_response.json()["id"]
        
        # Then get it
        response = client.get(f"/api/v1/resumes/{resume_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == resume_id
        assert data["filename"] == "test2.pdf"


class TestApplicationEndpoints:
    """Test application-related endpoints."""
    
    def test_create_application(self):
        """Test creating a job application."""
        # First create a job and resume
        job_response = client.post("/api/v1/jobs/extract", json={"url": "https://example.com/job"})
        job_id = job_response.json()["id"]
        
        files = {"file": ("test.pdf", b"fake pdf content", "application/pdf")}
        resume_response = client.post("/api/v1/resumes/upload", files=files)
        resume_id = resume_response.json()["id"]
        
        # Create application
        response = client.post("/api/v1/applications", json={
            "job_id": job_id,
            "resume_id": resume_id
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["job_id"] == job_id
        assert data["resume_id"] == resume_id
        assert "id" in data
    
    def test_get_application(self):
        """Test getting application by ID."""
        # First create an application
        job_response = client.post("/api/v1/jobs/extract", json={"url": "https://example.com/job2"})
        job_id = job_response.json()["id"]
        
        files = {"file": ("test2.pdf", b"fake pdf content", "application/pdf")}
        resume_response = client.post("/api/v1/resumes/upload", files=files)
        resume_id = resume_response.json()["id"]
        
        create_response = client.post("/api/v1/applications", json={
            "job_id": job_id,
            "resume_id": resume_id
        })
        app_id = create_response.json()["id"]
        
        # Then get it
        response = client.get(f"/api/v1/applications/{app_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == app_id
    
    def test_get_application_status(self):
        """Test getting application status."""
        # First create an application
        job_response = client.post("/api/v1/jobs/extract", json={"url": "https://example.com/job3"})
        job_id = job_response.json()["id"]
        
        files = {"file": ("test3.pdf", b"fake pdf content", "application/pdf")}
        resume_response = client.post("/api/v1/resumes/upload", files=files)
        resume_id = resume_response.json()["id"]
        
        create_response = client.post("/api/v1/applications", json={
            "job_id": job_id,
            "resume_id": resume_id
        })
        app_id = create_response.json()["id"]
        
        # Then get status
        response = client.get(f"/api/v1/applications/{app_id}/status")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == app_id


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "LaudatorAI API"
    
    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data


if __name__ == "__main__":
    pytest.main([__file__])
