#!/usr/bin/env python3
"""Test script to verify backend startup."""

import os
import sys
import time
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import fastapi
        print("✓ FastAPI imported successfully")
    except ImportError as e:
        print(f"✗ FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print("✓ Uvicorn imported successfully")
    except ImportError as e:
        print(f"✗ Uvicorn import failed: {e}")
        return False
    
    try:
        from app.main import app
        print("✓ Main app imported successfully")
    except ImportError as e:
        print(f"✗ Main app import failed: {e}")
        return False
    
    try:
        from app.core.config import settings
        print("✓ Settings imported successfully")
    except ImportError as e:
        print(f"✗ Settings import failed: {e}")
        return False
    
    return True

def test_environment():
    """Test environment variables."""
    print("\nTesting environment variables...")
    
    required_vars = ['DATABASE_URL', 'REDIS_URL']
    optional_vars = ['BACKEND_CORS_ORIGINS', 'ENVIRONMENT', 'DEBUG']
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✓ {var} is set")
        else:
            print(f"✗ {var} is not set (required)")
    
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"✓ {var} is set: {value}")
        else:
            print(f"- {var} is not set (optional)")
    
    return True

def test_app_creation():
    """Test if the FastAPI app can be created."""
    print("\nTesting app creation...")
    
    try:
        from app.main import app
        print("✓ FastAPI app created successfully")
        print(f"✓ App title: {app.title}")
        print(f"✓ App version: {app.version}")
        return True
    except Exception as e:
        print(f"✗ App creation failed: {e}")
        return False

def test_health_endpoint():
    """Test if the health endpoint works."""
    print("\nTesting health endpoint...")
    
    try:
        from app.main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        response = client.get("/health")
        
        if response.status_code == 200:
            print("✓ Health endpoint responds with 200")
            data = response.json()
            print(f"✓ Health response: {data}")
            return True
        else:
            print(f"✗ Health endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health endpoint test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("LaudatorAI Backend Startup Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_environment,
        test_app_creation,
        test_health_endpoint,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! Backend should start successfully.")
        return True
    else:
        print("✗ Some tests failed. Check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
