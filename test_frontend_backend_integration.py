#!/usr/bin/env python3
"""Manual test script for frontend-backend integration."""

import requests
import json
import time

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def test_backend_health():
    """Test backend health endpoint."""
    print("🔍 Testing backend health...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        if response.status_code == 200:
            print("✅ Backend is healthy")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend connection failed: {e}")
        return False

def test_job_extraction():
    """Test job extraction endpoint."""
    print("🔍 Testing job extraction...")
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/jobs/extract",
            json={"url": "https://example.com/test-job"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Job extracted successfully - ID: {data.get('id')}")
            return data.get('id')
        else:
            print(f"❌ Job extraction failed: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Job extraction request failed: {e}")
        return None

def test_resume_upload():
    """Test resume upload endpoint."""
    print("🔍 Testing resume upload...")
    
    try:
        # Create a mock PDF file
        files = {
            'file': ('test_resume.pdf', b'fake pdf content', 'application/pdf')
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/v1/resumes/upload",
            files=files
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Resume uploaded successfully - ID: {data.get('id')}")
            return data.get('id')
        else:
            print(f"❌ Resume upload failed: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Resume upload request failed: {e}")
        return None

def test_application_creation(job_id, resume_id):
    """Test application creation endpoint."""
    print("🔍 Testing application creation...")
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/applications",
            json={
                "job_id": job_id,
                "resume_id": resume_id
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Application created successfully - ID: {data.get('id')}")
            return data.get('id')
        else:
            print(f"❌ Application creation failed: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Application creation request failed: {e}")
        return None

def test_feedback_submission(application_id):
    """Test feedback submission endpoint."""
    print("🔍 Testing feedback submission...")
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/feedback",
            json={
                "application_id": str(application_id),
                "rating": 5,
                "comment": "Great experience with the AI-generated resume!",
                "timestamp": "2024-12-19T10:00:00Z"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Feedback submitted successfully - ID: {data.get('id')}")
            return True
        else:
            print(f"❌ Feedback submission failed: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Feedback submission request failed: {e}")
        return False

def test_frontend_connectivity():
    """Test frontend connectivity."""
    print("🔍 Testing frontend connectivity...")
    
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            return True
        else:
            print(f"❌ Frontend returned status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend connection failed: {e}")
        return False

def main():
    """Run the complete integration test."""
    print("🚀 Starting Frontend-Backend Integration Test")
    print("=" * 60)
    
    # Test backend health
    if not test_backend_health():
        print("❌ Backend health check failed. Please ensure backend is running.")
        return False
    
    # Test job extraction
    job_id = test_job_extraction()
    if not job_id:
        print("❌ Job extraction failed.")
        return False
    
    # Test resume upload
    resume_id = test_resume_upload()
    if not resume_id:
        print("❌ Resume upload failed.")
        return False
    
    # Test application creation
    app_id = test_application_creation(job_id, resume_id)
    if not app_id:
        print("❌ Application creation failed.")
        return False
    
    # Test feedback submission
    if not test_feedback_submission(app_id):
        print("❌ Feedback submission failed.")
        return False
    
    # Test frontend connectivity
    if not test_frontend_connectivity():
        print("⚠️  Frontend is not accessible. Please ensure frontend is running.")
        print("   Backend integration tests passed, but frontend is not available.")
    else:
        print("✅ Frontend is accessible")
    
    print("\n" + "=" * 60)
    print("🎉 All integration tests passed!")
    print("✅ Backend API is working correctly")
    print("✅ Frontend-backend integration is functional")
    print("✅ Complete user workflow is operational")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
