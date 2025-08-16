"""Complete integration tests for frontend-backend workflow."""

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
    """Test the complete frontend-backend integration workflow."""
    
    def test_complete_user_journey(self):
        """Test the complete user journey from job extraction to feedback."""
        print("🚀 Testing complete user journey...")
        
        # Step 1: Health check
        health_response = client.get("/health")
        assert health_response.status_code == 200
        print("✅ Health check passed")
        
        # Step 2: Extract job description (simulating frontend request)
        job_url = "https://example.com/software-engineer-position"
        job_response = client.post("/api/v1/jobs/extract", json={"url": job_url})
        assert job_response.status_code == 200
        job_data = job_response.json()
        job_id = job_data["id"]
        print(f"✅ Job extracted with ID: {job_id}")
        
        # Step 3: Upload resume (simulating frontend request)
        resume_content = b"fake resume content for testing"
        files = {"file": ("test_resume.pdf", resume_content, "application/pdf")}
        resume_response = client.post("/api/v1/resumes/upload", files=files)
        assert resume_response.status_code == 200
        resume_data = resume_response.json()
        resume_id = resume_data["id"]
        print(f"✅ Resume uploaded with ID: {resume_id}")
        
        # Step 4: Create application (simulating frontend request)
        app_response = client.post("/api/v1/applications", json={
            "job_id": job_id,
            "resume_id": resume_id
        })
        assert app_response.status_code == 200
        app_data = app_response.json()
        app_id = app_data["id"]
        print(f"✅ Application created with ID: {app_id}")
        
        # Step 5: Check application status
        status_response = client.get(f"/api/v1/applications/{app_id}/status")
        assert status_response.status_code == 200
        status_data = status_response.json()
        assert status_data["id"] == app_id
        print(f"✅ Application status checked: {status_data['status']}")
        
        # Step 6: Submit feedback (simulating frontend request)
        feedback_response = client.post("/api/v1/feedback", json={
            "application_id": str(app_id),
            "rating": 5,
            "comment": "Great experience! The AI-generated resume was perfect.",
            "timestamp": "2024-12-19T10:00:00Z"
        })
        assert feedback_response.status_code == 200
        feedback_data = feedback_response.json()
        print(f"✅ Feedback submitted with ID: {feedback_data['id']}")
        
        # Step 7: Get feedback statistics
        stats_response = client.get("/api/v1/feedback/stats")
        assert stats_response.status_code == 200
        stats_data = stats_response.json()
        assert "total_feedback" in stats_data
        print("✅ Feedback statistics retrieved")
        
        print("🎉 Complete user journey test passed!")


class TestFrontendBackendCompatibility:
    """Test that backend responses are compatible with frontend expectations."""
    
    def test_job_extraction_frontend_compatibility(self):
        """Test that job extraction response matches frontend expectations."""
        print("🔍 Testing job extraction frontend compatibility...")
        
        response = client.post("/api/v1/jobs/extract", json={"url": "https://example.com/test-job"})
        assert response.status_code == 200
        data = response.json()
        
        # Check all required fields that frontend expects
        required_fields = ["id", "title", "company", "location", "description", "requirements", "created_at"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        # Check data types
        assert isinstance(data["id"], int)
        assert isinstance(data["title"], str)
        assert isinstance(data["company"], str)
        assert isinstance(data["created_at"], str)
        
        print("✅ Job extraction response is frontend-compatible")
    
    def test_resume_upload_frontend_compatibility(self):
        """Test that resume upload response matches frontend expectations."""
        print("🔍 Testing resume upload frontend compatibility...")
        
        files = {"file": ("test.pdf", b"content", "application/pdf")}
        response = client.post("/api/v1/resumes/upload", files=files)
        assert response.status_code == 200
        data = response.json()
        
        # Check all required fields that frontend expects
        required_fields = ["id", "filename", "created_at"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        # Check data types
        assert isinstance(data["id"], int)
        assert isinstance(data["filename"], str)
        assert isinstance(data["created_at"], str)
        
        print("✅ Resume upload response is frontend-compatible")
    
    def test_application_creation_frontend_compatibility(self):
        """Test that application creation response matches frontend expectations."""
        print("🔍 Testing application creation frontend compatibility...")
        
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
        
        # Check all required fields that frontend expects
        required_fields = ["id", "job_id", "resume_id", "status", "created_at"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        # Check data types
        assert isinstance(data["id"], int)
        assert isinstance(data["job_id"], int)
        assert isinstance(data["resume_id"], int)
        assert isinstance(data["status"], str)
        assert isinstance(data["created_at"], str)
        
        print("✅ Application creation response is frontend-compatible")


class TestErrorHandlingIntegration:
    """Test error handling across the complete workflow."""
    
    def test_invalid_job_url_handling(self):
        """Test handling of invalid job URLs in the workflow."""
        print("🔍 Testing invalid job URL handling...")
        
        response = client.post("/api/v1/jobs/extract", json={"url": "not-a-valid-url"})
        assert response.status_code == 422  # Validation error
        
        print("✅ Invalid job URL properly handled")
    
    def test_invalid_file_type_handling(self):
        """Test handling of invalid file types in the workflow."""
        print("🔍 Testing invalid file type handling...")
        
        files = {"file": ("test.txt", b"text content", "text/plain")}
        response = client.post("/api/v1/resumes/upload", files=files)
        assert response.status_code == 400  # Bad request
        
        print("✅ Invalid file type properly handled")
    
    def test_missing_required_fields_handling(self):
        """Test handling of missing required fields."""
        print("🔍 Testing missing required fields handling...")
        
        # Test missing URL
        response = client.post("/api/v1/jobs/extract", json={})
        assert response.status_code == 422  # Validation error
        
        # Test missing job_id and resume_id
        response = client.post("/api/v1/applications", json={})
        assert response.status_code == 422  # Validation error
        
        print("✅ Missing required fields properly handled")
    
    def test_nonexistent_resource_handling(self):
        """Test handling of requests for nonexistent resources."""
        print("🔍 Testing nonexistent resource handling...")
        
        # Test nonexistent job
        response = client.get("/api/v1/jobs/99999")
        assert response.status_code == 404
        
        # Test nonexistent resume
        response = client.get("/api/v1/resumes/99999")
        assert response.status_code == 404
        
        # Test nonexistent application
        response = client.get("/api/v1/applications/99999")
        assert response.status_code == 404
        
        print("✅ Nonexistent resources properly handled")


class TestPerformanceIntegration:
    """Test performance characteristics of the integrated system."""
    
    def test_concurrent_requests_handling(self):
        """Test handling of concurrent requests."""
        print("🔍 Testing concurrent requests handling...")
        
        import threading
        import time
        
        results = []
        errors = []
        
        def make_request():
            try:
                response = client.get("/health")
                results.append(response.status_code)
            except Exception as e:
                errors.append(str(e))
        
        # Create multiple threads to make concurrent requests
        threads = []
        for i in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check results
        successful_requests = sum(1 for status in results if status == 200)
        assert successful_requests >= 8, f"Too many failed requests: {len(results) - successful_requests}"
        assert len(errors) == 0, f"Unexpected errors: {errors}"
        
        print(f"✅ Concurrent requests handled successfully: {successful_requests}/10")
    
    def test_response_time_consistency(self):
        """Test that response times are consistent."""
        print("🔍 Testing response time consistency...")
        
        response_times = []
        
        for i in range(5):
            start_time = time.time()
            response = client.get("/health")
            end_time = time.time()
            
            assert response.status_code == 200
            response_times.append(end_time - start_time)
        
        # Check that response times are reasonable (less than 1 second)
        max_response_time = max(response_times)
        assert max_response_time < 1.0, f"Response time too slow: {max_response_time}s"
        
        print(f"✅ Response times consistent: max {max_response_time:.3f}s")


if __name__ == "__main__":
    print("🚀 Starting complete integration tests...")
    
    # Run complete workflow test
    workflow_test = TestCompleteWorkflow()
    workflow_test.test_complete_user_journey()
    
    # Run frontend-backend compatibility tests
    compatibility_test = TestFrontendBackendCompatibility()
    compatibility_test.test_job_extraction_frontend_compatibility()
    compatibility_test.test_resume_upload_frontend_compatibility()
    compatibility_test.test_application_creation_frontend_compatibility()
    
    # Run error handling tests
    error_test = TestErrorHandlingIntegration()
    error_test.test_invalid_job_url_handling()
    error_test.test_invalid_file_type_handling()
    error_test.test_missing_required_fields_handling()
    error_test.test_nonexistent_resource_handling()
    
    # Run performance tests
    perf_test = TestPerformanceIntegration()
    perf_test.test_concurrent_requests_handling()
    perf_test.test_response_time_consistency()
    
    print("🎉 All complete integration tests passed!")
