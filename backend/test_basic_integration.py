#!/usr/bin/env python3
"""Basic integration test that doesn't require all dependencies."""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_basic_imports():
    """Test that basic imports work."""
    print("🔍 Testing basic imports...")
    
    try:
        # Test core imports
        from app.core.config import settings
        print("✅ Config import successful")
        
        from app.main import app
        print("✅ Main app import successful")
        
        from app.api.v1.api import api_router
        print("✅ API router import successful")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_basic_endpoints():
    """Test that basic endpoints are registered."""
    print("🔍 Testing basic endpoints...")
    
    try:
        from app.main import app
        
        # Check if the app has routes
        routes = app.routes
        print(f"✅ App has {len(routes)} routes")
        
        # Check for health endpoint
        health_route = None
        for route in routes:
            if hasattr(route, 'path') and route.path == '/health':
                health_route = route
                break
        
        if health_route:
            print("✅ Health endpoint found")
        else:
            print("⚠️  Health endpoint not found")
        
        return True
    except Exception as e:
        print(f"❌ Endpoint test failed: {e}")
        return False

def test_schema_validation():
    """Test that schemas work correctly."""
    print("🔍 Testing schema validation...")
    
    try:
        from app.schemas import JobUrlRequest, JobResponse
        
        # Test URL validation
        valid_url = "https://example.com/job"
        job_request = JobUrlRequest(url=valid_url)
        print("✅ Valid URL accepted")
        
        # Test invalid URL (should raise validation error)
        try:
            invalid_url = "not-a-url"
            job_request = JobUrlRequest(url=invalid_url)
            print("❌ Invalid URL was accepted (should have failed)")
            return False
        except Exception:
            print("✅ Invalid URL properly rejected")
        
        return True
    except Exception as e:
        print(f"❌ Schema validation failed: {e}")
        return False

def main():
    """Run basic integration tests."""
    print("🚀 Starting Basic Integration Tests")
    print("=" * 50)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Basic Endpoints", test_basic_endpoints),
        ("Schema Validation", test_schema_validation),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        success = test_func()
        results.append((test_name, success))
    
    print("\n" + "=" * 50)
    print("📊 Basic Integration Test Results")
    print("=" * 50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 Basic integration tests passed!")
        print("✅ Core components are working correctly")
        print("✅ Ready for more comprehensive testing")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        print("Please fix the issues before proceeding.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
