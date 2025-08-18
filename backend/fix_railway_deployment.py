#!/usr/bin/env python3
"""Script to diagnose and fix Railway deployment issues."""

import os
import sys
import json
from pathlib import Path

def check_environment_variables():
    """Check if required environment variables are set."""
    print("🔍 Checking Environment Variables...")
    
    required_vars = {
        'DATABASE_URL': 'PostgreSQL connection string (auto-provided by Railway)',
        'REDIS_URL': 'Redis connection string (auto-provided by Railway)',
    }
    
    optional_vars = {
        'BACKEND_CORS_ORIGINS': 'CORS origins (e.g., https://your-frontend.vercel.app)',
        'ENVIRONMENT': 'Environment (production/development)',
        'DEBUG': 'Debug mode (true/false)',
        'OPENAI_API_KEY': 'OpenAI API key (optional)',
    }
    
    missing_required = []
    missing_optional = []
    
    for var, description in required_vars.items():
        if os.getenv(var):
            print(f"✅ {var}: Set")
        else:
            print(f"❌ {var}: Missing - {description}")
            missing_required.append(var)
    
    for var, description in optional_vars.items():
        if os.getenv(var):
            print(f"✅ {var}: Set")
        else:
            print(f"⚠️  {var}: Missing - {description}")
            missing_optional.append(var)
    
    return missing_required, missing_optional

def check_railway_config():
    """Check Railway configuration files."""
    print("\n🔍 Checking Railway Configuration...")
    
    railway_json = Path("railway.json")
    if railway_json.exists():
        print("✅ railway.json exists")
        try:
            with open(railway_json) as f:
                config = json.load(f)
            print(f"✅ Health check path: {config.get('deploy', {}).get('healthcheckPath', 'Not set')}")
            print(f"✅ Start command: {config.get('deploy', {}).get('startCommand', 'Not set')}")
        except Exception as e:
            print(f"❌ Error reading railway.json: {e}")
    else:
        print("❌ railway.json missing")
    
    start_py = Path("start.py")
    if start_py.exists():
        print("✅ start.py exists")
    else:
        print("❌ start.py missing")

def check_dependencies():
    """Check if required dependencies are available."""
    print("\n🔍 Checking Dependencies...")
    
    dependencies = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'redis',
        'pydantic',
        'pydantic-settings'
    ]
    
    missing_deps = []
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep}")
            missing_deps.append(dep)
    
    return missing_deps

def generate_railway_variables_template():
    """Generate a template for Railway environment variables."""
    print("\n📝 Railway Environment Variables Template:")
    print("=" * 50)
    print("Add these to your Railway service Variables tab:")
    print()
    
    template = {
        "BACKEND_CORS_ORIGINS": "https://your-frontend-domain.vercel.app,http://localhost:3000",
        "ENVIRONMENT": "production",
        "DEBUG": "false",
        "OPENAI_API_KEY": "your-openai-api-key-here"
    }
    
    for key, value in template.items():
        print(f"{key}={value}")
    
    print()
    print("Note: DATABASE_URL and REDIS_URL are automatically provided by Railway")
    print("when you add PostgreSQL and Redis services to your project.")

def check_health_endpoint():
    """Test the health endpoint."""
    print("\n🔍 Testing Health Endpoint...")
    
    try:
        from app.main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        response = client.get("/health")
        
        if response.status_code == 200:
            print("✅ Health endpoint responds with 200")
            data = response.json()
            print(f"✅ Response: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"❌ Health endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint test failed: {e}")
        return False

def main():
    """Main diagnostic function."""
    print("🚀 LaudatorAI Railway Deployment Diagnostic")
    print("=" * 50)
    
    # Check environment variables
    missing_required, missing_optional = check_environment_variables()
    
    # Check Railway configuration
    check_railway_config()
    
    # Check dependencies
    missing_deps = check_dependencies()
    
    # Test health endpoint
    health_ok = check_health_endpoint()
    
    # Generate recommendations
    print("\n📋 Recommendations:")
    print("=" * 50)
    
    if missing_required:
        print("❌ CRITICAL: Missing required environment variables:")
        for var in missing_required:
            print(f"   - {var}")
        print("\n   Solution: Add PostgreSQL and Redis services to your Railway project")
    
    if missing_optional:
        print("⚠️  WARNING: Missing optional environment variables:")
        for var in missing_optional:
            print(f"   - {var}")
    
    if missing_deps:
        print("❌ CRITICAL: Missing dependencies:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\n   Solution: Check requirements.txt and rebuild")
    
    if not health_ok:
        print("❌ CRITICAL: Health endpoint not working")
        print("   Solution: Check application startup and logs")
    
    if not missing_required and not missing_deps and health_ok:
        print("✅ All checks passed! Your deployment should work.")
    else:
        print("\n🔧 Quick Fix Steps:")
        print("1. Add PostgreSQL service to Railway project")
        print("2. Add Redis service to Railway project")
        print("3. Set BACKEND_CORS_ORIGINS in Railway variables")
        print("4. Redeploy the service")
        
        generate_railway_variables_template()

if __name__ == "__main__":
    main()
