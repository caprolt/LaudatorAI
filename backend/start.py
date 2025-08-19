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
    
    # Debug environment variables (without sensitive data)
    logger.info("Environment variable check:")
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive parts of URLs
            if 'DATABASE_URL' in var and value:
                masked_url = value.split('@')[0] + '@***' if '@' in value else '***'
                logger.info(f"  {var}: {masked_url}")
            elif 'REDIS_URL' in var and value:
                masked_url = value.split('@')[0] + '@***' if '@' in value else '***'
                logger.info(f"  {var}: {masked_url}")
            else:
                logger.info(f"  {var}: [SET]")
        else:
            logger.warning(f"  {var}: [MISSING]")
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {missing_vars}")
        logger.warning("Application may not function properly without these variables")
        logger.warning("Add PostgreSQL and Redis services to your Railway project")
        logger.warning("Make sure services are properly linked in Railway dashboard")
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

def fix_railway_database_url():
    """Fix Railway DATABASE_URL if it contains internal hostname."""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        return
    
    # Check if URL contains Railway internal hostname
    if 'railway.internal' in database_url:
        logger.warning("Detected Railway internal hostname in DATABASE_URL")
        logger.warning("This URL is only accessible from within Railway's network")
        logger.warning("Make sure your Railway services are properly linked")
        logger.warning("If testing locally, you may need to use external connection details")
        return False
    
    return True

def test_database_connection():
    """Test database connection if DATABASE_URL is available."""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        logger.warning("DATABASE_URL not set, skipping database connection test")
        return True
    
    # Check for Railway internal hostname issues
    if not fix_railway_database_url():
        logger.error("Cannot test database connection with internal Railway hostname")
        return False
    
    try:
        from sqlalchemy import create_engine, text
        from sqlalchemy.exc import SQLAlchemyError
        
        # Log connection attempt (without sensitive data)
        if '@' in database_url:
            host_part = database_url.split('@')[1].split('/')[0]
            logger.info(f"Attempting database connection to: {host_part}")
        else:
            logger.info("Attempting database connection...")
        
        engine = create_engine(database_url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection test passed")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Database connection test failed: {e}")
        logger.error("This usually means:")
        logger.error("  1. Railway PostgreSQL service is not properly linked")
        logger.error("  2. DATABASE_URL contains internal hostname that's not accessible")
        logger.error("  3. Database credentials are incorrect")
        logger.error("  4. Database service is not running")
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
        # Check for Railway-specific issues first
        fix_railway_database_url()
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
