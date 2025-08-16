#!/usr/bin/env python3
"""Simplified integration test focusing on core functionality."""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_config():
    """Test configuration loading."""
    print("🔍 Testing configuration...")
    
    try:
        from app.core.config import settings
        print(f"✅ Config loaded - API_V1_STR: {settings.API_V1_STR}")
        print(f"✅ Config loaded - PROJECT_NAME: {settings.PROJECT_NAME}")
        return True
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_schemas():
    """Test schema definitions."""
    print("🔍 Testing schemas...")
    
    try:
        from app.schemas import JobUrlRequest, JobResponse, ResumeResponse, JobApplicationResponse
        
        # Test JobUrlRequest
        valid_url = "https://example.com/job"
        job_request = JobUrlRequest(url=valid_url)
        print("✅ JobUrlRequest schema works")
        
        # Test that invalid URL raises error
        try:
            invalid_url = "not-a-url"
            job_request = JobUrlRequest(url=invalid_url)
            print("❌ Invalid URL was accepted (should have failed)")
            return False
        except Exception:
            print("✅ Invalid URL properly rejected")
        
        return True
    except Exception as e:
        print(f"❌ Schema test failed: {e}")
        return False

def test_api_structure():
    """Test API structure without importing the full app."""
    print("🔍 Testing API structure...")
    
    try:
        # Test that we can import the API router
        from app.api.v1.api import api_router
        print("✅ API router imported successfully")
        
        # Test that we can import individual endpoints
        from app.api.v1.endpoints import health, jobs, resumes, applications, feedback
        print("✅ All endpoint modules imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ API structure test failed: {e}")
        return False

def test_endpoint_definitions():
    """Test that endpoints are properly defined."""
    print("🔍 Testing endpoint definitions...")
    
    try:
        from app.api.v1.endpoints.health import router as health_router
        from app.api.v1.endpoints.jobs import router as jobs_router
        from app.api.v1.endpoints.resumes import router as resumes_router
        from app.api.v1.endpoints.applications import router as applications_router
        from app.api.v1.endpoints.feedback import router as feedback_router
        
        print("✅ All endpoint routers imported successfully")
        
        # Check that routers have routes
        routers = [
            ("Health", health_router),
            ("Jobs", jobs_router),
            ("Resumes", resumes_router),
            ("Applications", applications_router),
            ("Feedback", feedback_router),
        ]
        
        for name, router in routers:
            if hasattr(router, 'routes') and router.routes:
                print(f"✅ {name} router has {len(router.routes)} routes")
            else:
                print(f"⚠️  {name} router has no routes")
        
        return True
    except Exception as e:
        print(f"❌ Endpoint definitions test failed: {e}")
        return False

def test_frontend_compatibility():
    """Test that backend schemas are compatible with frontend expectations."""
    print("🔍 Testing frontend compatibility...")
    
    try:
        from app.schemas import JobResponse, ResumeResponse, JobApplicationResponse
        
        # Test that JobResponse has all required fields
        required_job_fields = ["id", "title", "company", "location", "description", "requirements", "created_at"]
        job_fields = JobResponse.__fields__.keys()
        
        missing_job_fields = [field for field in required_job_fields if field not in job_fields]
        if missing_job_fields:
            print(f"❌ JobResponse missing fields: {missing_job_fields}")
            return False
        else:
            print("✅ JobResponse has all required fields")
        
        # Test that ResumeResponse has all required fields
        required_resume_fields = ["id", "filename", "created_at"]
        resume_fields = ResumeResponse.__fields__.keys()
        
        missing_resume_fields = [field for field in required_resume_fields if field not in resume_fields]
        if missing_resume_fields:
            print(f"❌ ResumeResponse missing fields: {missing_resume_fields}")
            return False
        else:
            print("✅ ResumeResponse has all required fields")
        
        # Test that JobApplicationResponse has all required fields
        required_app_fields = ["id", "job_id", "resume_id", "status", "created_at"]
        app_fields = JobApplicationResponse.__fields__.keys()
        
        missing_app_fields = [field for field in required_app_fields if field not in app_fields]
        if missing_app_fields:
            print(f"❌ JobApplicationResponse missing fields: {missing_app_fields}")
            return False
        else:
            print("✅ JobApplicationResponse has all required fields")
        
        return True
    except Exception as e:
        print(f"❌ Frontend compatibility test failed: {e}")
        return False

def main():
    """Run simplified integration tests."""
    print("🚀 Starting Simplified Integration Tests")
    print("=" * 60)
    
    tests = [
        ("Configuration", test_config),
        ("Schemas", test_schemas),
        ("API Structure", test_api_structure),
        ("Endpoint Definitions", test_endpoint_definitions),
        ("Frontend Compatibility", test_frontend_compatibility),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        success = test_func()
        results.append((test_name, success))
    
    print("\n" + "=" * 60)
    print("📊 Simplified Integration Test Results")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 Simplified integration tests passed!")
        print("✅ Core components are working correctly")
        print("✅ API structure is properly defined")
        print("✅ Frontend-backend compatibility is maintained")
        print("✅ Ready for Phase 8 (Deployment)")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        print("Please fix the issues before proceeding to Phase 8.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
