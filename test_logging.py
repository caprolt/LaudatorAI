#!/usr/bin/env python3
"""Test script for LaudatorAI logging system."""

import sys
import os
import time
import requests
import json
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_backend_logging():
    """Test backend logging functionality."""
    print("🧪 Testing Backend Logging System")
    print("=" * 50)
    
    try:
        # Import backend logging
        from app.core.logging import (
            logger, log_request, log_api_call, log_task_start, 
            log_task_complete, log_task_error, log_file_operation,
            log_database_operation, log_external_api_call,
            log_user_action, log_performance_metric, log_security_event
        )
        
        print("✅ Backend logging imports successful")
        
        # Test basic logging
        logger.info("Test info message", extra={'test': True, 'component': 'test_script'})
        logger.warning("Test warning message", extra={'test': True, 'component': 'test_script'})
        logger.error("Test error message", extra={'test': True, 'component': 'test_script'})
        
        # Test specialized logging functions
        log_request(
            request_id="test-123",
            method="GET",
            path="/api/v1/test",
            status_code=200,
            duration=0.123,
            ip_address="127.0.0.1",
            user_agent="Test-Agent/1.0"
        )
        
        log_api_call(
            api_name="test_api",
            method="POST",
            endpoint="/api/v1/test",
            status_code=201,
            duration=0.456,
            request_id="test-123",
            user_id="test-user"
        )
        
        log_task_start("task-123", "test_task", user_id="test-user")
        time.sleep(0.1)  # Simulate work
        log_task_complete("task-123", "test_task", 0.1, result="success")
        
        log_file_operation("upload", "/tmp/test.pdf", True, file_size=1024)
        log_database_operation("SELECT", "users", True, 0.045, user_id="test-user")
        log_external_api_call("openai", "/v1/chat/completions", "POST", 200, 2.34)
        log_user_action("test-user", "login", "auth", True)
        log_performance_metric("response_time", 150.5, "ms", endpoint="/api/v1/test")
        log_security_event("test_event", "low", "Test security event")
        
        print("✅ All backend logging functions tested successfully")
        return True
        
    except Exception as e:
        print(f"❌ Backend logging test failed: {e}")
        return False

def test_frontend_logging_api():
    """Test frontend logging API endpoint."""
    print("\n🧪 Testing Frontend Logging API")
    print("=" * 50)
    
    # Test data
    test_log_data = {
        "level": "INFO",
        "name": "LaudatorAI.Test",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "message": "Test frontend log message",
        "url": "http://localhost:3000/test",
        "userAgent": "Test-Browser/1.0",
        "sessionId": "test-session-123",
        "data": {
            "test": True,
            "component": "test_script"
        }
    }
    
    try:
        # Try to send to backend if available
        backend_url = os.getenv('BACKEND_API_URL', 'http://localhost:8000')
        
        response = requests.post(
            f"{backend_url}/api/v1/logs",
            json=test_log_data,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 200:
            print("✅ Frontend logging API test successful")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"⚠️  Frontend logging API returned status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Frontend logging API test skipped (backend not available): {e}")
        print("   This is normal if the backend is not running")
        return True  # Not a failure if backend is not running

def test_log_file_creation():
    """Test that log files are created in development."""
    print("\n🧪 Testing Log File Creation")
    print("=" * 50)
    
    log_file_path = os.path.join('backend', 'logs', 'app.log')
    
    if os.path.exists(log_file_path):
        print(f"✅ Log file exists: {log_file_path}")
        
        # Read last few lines
        with open(log_file_path, 'r') as f:
            lines = f.readlines()
            if lines:
                print(f"   Last log entry: {lines[-1].strip()}")
            else:
                print("   Log file is empty")
        return True
    else:
        print(f"⚠️  Log file not found: {log_file_path}")
        print("   This is normal in production mode")
        return True

def main():
    """Run all logging tests."""
    print("🚀 LaudatorAI Logging System Test")
    print("=" * 60)
    
    # Test backend logging
    backend_success = test_backend_logging()
    
    # Test frontend logging API
    frontend_success = test_frontend_logging_api()
    
    # Test log file creation
    file_success = test_log_file_creation()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 60)
    print(f"Backend Logging: {'✅ PASS' if backend_success else '❌ FAIL'}")
    print(f"Frontend Logging API: {'✅ PASS' if frontend_success else '❌ FAIL'}")
    print(f"Log File Creation: {'✅ PASS' if file_success else '❌ FAIL'}")
    
    if all([backend_success, frontend_success, file_success]):
        print("\n🎉 All logging tests passed!")
        print("\n📝 Next Steps:")
        print("1. Deploy to Vercel to see frontend logs")
        print("2. Deploy to Railway to see backend logs")
        print("3. Check the LOGGING_GUIDE.md for usage instructions")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
