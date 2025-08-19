#!/usr/bin/env python3
"""Startup script for LaudatorAI backend."""

import os
import sys
import time
import logging
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Set up basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_environment():
    """Check if required environment variables are set."""
    required_vars = [
        'DATABASE_URL',
        'REDIS_URL',
    ]
    
    # Set defaults for Railway requirements
    if not os.getenv('PORT'):
        os.environ['PORT'] = '8000'
        logger.info("Set default PORT=8000")
    
    if not os.getenv('HOST'):
        os.environ['HOST'] = '0.0.0.0'
        logger.info("Set default HOST=0.0.0.0")
    
    if not os.getenv('ENVIRONMENT'):
        os.environ['ENVIRONMENT'] = 'production'
        logger.info("Set default ENVIRONMENT=production")
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {missing_vars}")
        logger.warning("Application may not function properly without these variables")
        logger.warning("Add PostgreSQL and Redis services to your Railway project")
        return False
    
    logger.info("Environment variables check passed")
    return True

def check_dependencies():
    """Check if required dependencies are available."""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import redis
        logger.info("All required dependencies are available")
        return True
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        return False

def test_database_connection():
    """Test database connection if DATABASE_URL is available."""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        logger.warning("DATABASE_URL not set, skipping database connection test")
        return True
    
    try:
        from sqlalchemy import create_engine, text
        from sqlalchemy.exc import SQLAlchemyError
        
        engine = create_engine(database_url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection test passed")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Database connection test failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during database test: {e}")
        return False

def test_redis_connection():
    """Test Redis connection if REDIS_URL is available."""
    redis_url = os.getenv('REDIS_URL')
    if not redis_url:
        logger.warning("REDIS_URL not set, skipping Redis connection test")
        return True
    
    try:
        import redis
        r = redis.from_url(redis_url)
        r.ping()
        logger.info("Redis connection test passed")
        return True
    except Exception as e:
        logger.error(f"Redis connection test failed: {e}")
        return False

def main():
    """Main startup function."""
    logger.info("Starting LaudatorAI backend...")
    
    # Print environment info for debugging
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info(f"Debug mode: {os.getenv('DEBUG', 'false')}")
    logger.info(f"Python version: {sys.version}")
    
    # Check environment variables
    env_ok = check_environment()
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Test connections (but don't fail startup if they fail)
    if env_ok:
        test_database_connection()
        test_redis_connection()
    
    # Import and start the application
    try:
        import uvicorn
        from app.main import app
        
        port = int(os.getenv('PORT', 8000))
        host = os.getenv('HOST', '0.0.0.0')
        
        logger.info(f"Starting server on {host}:{port}")
        logger.info(f"Health check endpoint: http://{host}:{port}/health")
        
        # Start the server
        uvicorn.run(
            app,
            host=host,
            port=port,
            workers=1,  # Use single worker for Railway
            log_level="info",
            access_log=True
        )
        
    except ImportError as e:
        logger.error(f"Failed to import required modules: {e}")
        logger.error("Please ensure all dependencies are installed")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    main()
