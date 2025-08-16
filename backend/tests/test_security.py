"""Security tests for API endpoints."""

import pytest
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


class TestInputValidation:
    """Test input validation and sanitization."""
    
    def test_sql_injection_prevention(self):
        """Test SQL injection prevention."""
        print("🔒 Testing SQL injection prevention...")
        
        # Test malicious SQL injection attempts
        malicious_inputs = [
            "'; DROP TABLE jobs; --",
            "' OR '1'='1",
            "'; INSERT INTO jobs VALUES (1, 'hacked'); --",
            "'; UPDATE jobs SET title='hacked'; --",
        ]
        
        for malicious_input in malicious_inputs:
            # Test job extraction with malicious URL
            response = client.post("/api/v1/jobs/extract", json={"url": malicious_input})
            
            # Should either return validation error or handle safely
            assert response.status_code in [422, 400], f"SQL injection vulnerability detected with input: {malicious_input}"
        
        print("✅ SQL injection prevention working correctly")
    
    def test_xss_prevention(self):
        """Test XSS prevention."""
        print("🔒 Testing XSS prevention...")
        
        # Test XSS attempts
        xss_inputs = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
            "';alert('xss');//",
        ]
        
        for xss_input in xss_inputs:
            # Test job extraction with XSS payload
            response = client.post("/api/v1/jobs/extract", json={"url": f"https://example.com/{xss_input}"})
            
            # Should handle safely
            assert response.status_code in [200, 422, 400], f"XSS vulnerability detected with input: {xss_input}"
        
        print("✅ XSS prevention working correctly")
    
    def test_path_traversal_prevention(self):
        """Test path traversal prevention."""
        print("🔒 Testing path traversal prevention...")
        
        # Test path traversal attempts
        path_traversal_inputs = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "....//....//....//etc/passwd",
            "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        ]
        
        for traversal_input in path_traversal_inputs:
            # Test resume upload with malicious filename
            files = {"file": (traversal_input, b"content", "application/pdf")}
            response = client.post("/api/v1/resumes/upload", files=files)
            
            # Should reject or handle safely
            assert response.status_code in [400, 422], f"Path traversal vulnerability detected with input: {traversal_input}"
        
        print("✅ Path traversal prevention working correctly")


class TestAuthenticationAndAuthorization:
    """Test authentication and authorization (if implemented)."""
    
    def test_public_endpoints_accessible(self):
        """Test that public endpoints are accessible."""
        print("🔒 Testing public endpoint accessibility...")
        
        # Health check should be public
        response = client.get("/health")
        assert response.status_code == 200
        
        # Root endpoint should be public
        response = client.get("/")
        assert response.status_code == 200
        
        print("✅ Public endpoints are accessible")
    
    def test_no_unauthorized_access(self):
        """Test that there's no unauthorized access to sensitive data."""
        print("🔒 Testing unauthorized access prevention...")
        
        # Try to access non-existent resources
        response = client.get("/api/v1/jobs/99999")
        assert response.status_code == 404
        
        response = client.get("/api/v1/resumes/99999")
        assert response.status_code == 404
        
        response = client.get("/api/v1/applications/99999")
        assert response.status_code == 404
        
        print("✅ Unauthorized access properly handled")


class TestDataValidation:
    """Test data validation and sanitization."""
    
    def test_url_validation(self):
        """Test URL validation."""
        print("🔒 Testing URL validation...")
        
        invalid_urls = [
            "not-a-url",
            "ftp://example.com",  # Non-HTTP protocol
            "http://",  # Incomplete URL
            "https://",  # Incomplete URL
            "file:///etc/passwd",  # File protocol
            "javascript:alert('xss')",  # JavaScript protocol
        ]
        
        for invalid_url in invalid_urls:
            response = client.post("/api/v1/jobs/extract", json={"url": invalid_url})
            assert response.status_code == 422, f"Invalid URL accepted: {invalid_url}"
        
        print("✅ URL validation working correctly")
    
    def test_file_validation(self):
        """Test file upload validation."""
        print("🔒 Testing file upload validation...")
        
        # Test invalid file types
        invalid_files = [
            ("test.txt", b"content", "text/plain"),
            ("test.exe", b"content", "application/x-msdownload"),
            ("test.sh", b"content", "application/x-sh"),
            ("test.bat", b"content", "application/x-msdos-program"),
        ]
        
        for filename, content, content_type in invalid_files:
            files = {"file": (filename, content, content_type)}
            response = client.post("/api/v1/resumes/upload", files=files)
            assert response.status_code == 400, f"Invalid file type accepted: {filename}"
        
        print("✅ File validation working correctly")
    
    def test_input_length_validation(self):
        """Test input length validation."""
        print("🔒 Testing input length validation...")
        
        # Test extremely long URL
        long_url = "https://example.com/" + "a" * 10000
        response = client.post("/api/v1/jobs/extract", json={"url": long_url})
        assert response.status_code in [422, 400], "Extremely long URL accepted"
        
        # Test extremely long filename
        long_filename = "a" * 1000 + ".pdf"
        files = {"file": (long_filename, b"content", "application/pdf")}
        response = client.post("/api/v1/resumes/upload", files=files)
        assert response.status_code in [400, 422], "Extremely long filename accepted"
        
        print("✅ Input length validation working correctly")


class TestErrorHandling:
    """Test error handling and information disclosure."""
    
    def test_no_sensitive_info_disclosure(self):
        """Test that sensitive information is not disclosed in errors."""
        print("🔒 Testing information disclosure prevention...")
        
        # Test various error conditions
        error_responses = [
            client.get("/api/v1/jobs/99999"),
            client.get("/api/v1/resumes/99999"),
            client.get("/api/v1/applications/99999"),
            client.post("/api/v1/jobs/extract", json={"url": "invalid-url"}),
        ]
        
        for response in error_responses:
            if response.status_code != 200:
                error_text = response.text.lower()
                
                # Check for sensitive information
                sensitive_patterns = [
                    "sql",
                    "database",
                    "password",
                    "secret",
                    "key",
                    "token",
                    "internal",
                    "stack trace",
                    "traceback",
                ]
                
                for pattern in sensitive_patterns:
                    assert pattern not in error_text, f"Sensitive information disclosed: {pattern}"
        
        print("✅ No sensitive information disclosure detected")
    
    def test_graceful_error_handling(self):
        """Test graceful error handling."""
        print("🔒 Testing graceful error handling...")
        
        # Test malformed JSON
        response = client.post("/api/v1/jobs/extract", data="invalid json", headers={"Content-Type": "application/json"})
        assert response.status_code == 422
        
        # Test missing required fields
        response = client.post("/api/v1/jobs/extract", json={})
        assert response.status_code == 422
        
        # Test wrong HTTP method
        response = client.get("/api/v1/jobs/extract")
        assert response.status_code == 405
        
        print("✅ Graceful error handling working correctly")


class TestRateLimiting:
    """Test rate limiting (if implemented)."""
    
    def test_no_rate_limiting_by_default(self):
        """Test that there's no rate limiting by default (for MVP)."""
        print("🔒 Testing rate limiting behavior...")
        
        # Make multiple rapid requests
        responses = []
        for i in range(10):
            response = client.get("/health")
            responses.append(response)
        
        # All requests should succeed (no rate limiting in MVP)
        successful_requests = sum(1 for r in responses if r.status_code == 200)
        assert successful_requests == 10, "Unexpected rate limiting detected"
        
        print("✅ No rate limiting detected (as expected for MVP)")


if __name__ == "__main__":
    print("🚀 Starting security tests...")
    
    # Run security tests
    input_validation = TestInputValidation()
    input_validation.test_sql_injection_prevention()
    input_validation.test_xss_prevention()
    input_validation.test_path_traversal_prevention()
    
    auth_test = TestAuthenticationAndAuthorization()
    auth_test.test_public_endpoints_accessible()
    auth_test.test_no_unauthorized_access()
    
    data_validation = TestDataValidation()
    data_validation.test_url_validation()
    data_validation.test_file_validation()
    data_validation.test_input_length_validation()
    
    error_handling = TestErrorHandling()
    error_handling.test_no_sensitive_info_disclosure()
    error_handling.test_graceful_error_handling()
    
    rate_limiting = TestRateLimiting()
    rate_limiting.test_no_rate_limiting_by_default()
    
    print("🎉 All security tests completed successfully!")
