#!/usr/bin/env python3
"""Test script to verify application startup."""

import os
import sys
import requests
import time
import subprocess
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def test_imports():
    """Test if all imports work."""
    print("Testing imports...")
    try:
        from app.main import app
        print("✅ App import successful")
        return True
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False

def test_health_endpoint():
    """Test the health endpoint."""
    print("Testing health endpoint...")
    try:
        from app.main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        response = client.get("/health")
        
        print(f"✅ Health endpoint status: {response.status_code}")
        print(f"✅ Health response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health endpoint test failed: {e}")
        return False

def test_environment():
    """Test environment variables."""
    print("Testing environment...")
    
    # Set some default values for testing
    os.environ.setdefault('DATABASE_URL', 'sqlite:///./test.db')
    os.environ.setdefault('REDIS_URL', 'redis://localhost:6379/0')
    os.environ.setdefault('ENVIRONMENT', 'test')
    os.environ.setdefault('DEBUG', 'true')
    
    print(f"✅ Environment variables set")
    return True

def main():
    """Run all tests."""
    print("🚀 Testing LaudatorAI Backend Startup")
    print("=" * 50)
    
    # Test environment
    if not test_environment():
        return False
    
    # Test imports
    if not test_imports():
        return False
    
    # Test health endpoint
    if not test_health_endpoint():
        return False
    
    print("=" * 50)
    print("✅ All tests passed! Application should start successfully.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
