#!/usr/bin/env python3
"""Debug script for Railway deployment issues."""

import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_environment_variables():
    """Check if required environment variables are set."""
    logger.info("=== Environment Variables Check ===")
    
    required_vars = [
        'DATABASE_URL',
        'REDIS_URL',
        'ENVIRONMENT',
        'PORT',
        'HOST'
    ]
    
    optional_vars = [
        'BACKEND_CORS_ORIGINS',
        'OPENAI_API_KEY',
        'MINIO_ENDPOINT',
        'MINIO_ACCESS_KEY',
        'MINIO_SECRET_KEY'
    ]
    
    all_vars = required_vars + optional_vars
    
    for var in all_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if 'KEY' in var or 'PASSWORD' in var or 'SECRET' in var:
                masked_value = value[:10] + "..." if len(value) > 10 else "***"
                logger.info(f"✓ {var}: {masked_value}")
            else:
                logger.info(f"✓ {var}: {value}")
        else:
            if var in required_vars:
                logger.error(f"✗ {var}: NOT SET (REQUIRED)")
            else:
                logger.warning(f"⚠ {var}: NOT SET (OPTIONAL)")

def test_imports():
    """Test if all required modules can be imported."""
    logger.info("=== Import Test ===")
    
    modules = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'redis',
        'celery',
        'pydantic',
        'pydantic_settings'
    ]
    
    for module in modules:
        try:
            __import__(module)
            logger.info(f"✓ {module}: imported successfully")
        except ImportError as e:
            logger.error(f"✗ {module}: import failed - {e}")

def test_database_connection():
    """Test database connection if DATABASE_URL is available."""
    logger.info("=== Database Connection Test ===")
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        logger.warning("DATABASE_URL not set, skipping database test")
        return
    
    try:
        from sqlalchemy import create_engine
        from sqlalchemy.exc import SQLAlchemyError
        
        logger.info("Attempting to connect to database...")
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            logger.info("✓ Database connection successful")
            
    except SQLAlchemyError as e:
        logger.error(f"✗ Database connection failed: {e}")
    except Exception as e:
        logger.error(f"✗ Unexpected error during database test: {e}")

def test_redis_connection():
    """Test Redis connection if REDIS_URL is available."""
    logger.info("=== Redis Connection Test ===")
    
    redis_url = os.getenv('REDIS_URL')
    if not redis_url:
        logger.warning("REDIS_URL not set, skipping Redis test")
        return
    
    try:
        import redis
        logger.info("Attempting to connect to Redis...")
        r = redis.from_url(redis_url)
        r.ping()
        logger.info("✓ Redis connection successful")
    except Exception as e:
        logger.error(f"✗ Redis connection failed: {e}")

def test_app_startup():
    """Test if the FastAPI app can be created."""
    logger.info("=== App Startup Test ===")
    
    try:
        from app.main import app
        logger.info("✓ FastAPI app created successfully")
        
        # Test if we can access the app's routes
        routes = [route.path for route in app.routes]
        logger.info(f"✓ App has {len(routes)} routes")
        logger.info(f"Routes: {routes[:5]}...")  # Show first 5 routes
        
    except Exception as e:
        logger.error(f"✗ App startup failed: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")

def main():
    """Run all debug checks."""
    logger.info("Starting Railway Debug Checks...")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Current working directory: {os.getcwd()}")
    
    check_environment_variables()
    test_imports()
    test_database_connection()
    test_redis_connection()
    test_app_startup()
    
    logger.info("=== Debug Checks Complete ===")

if __name__ == "__main__":
    main()
