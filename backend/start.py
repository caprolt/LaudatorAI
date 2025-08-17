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
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {missing_vars}")
        return False
    
    logger.info("Environment variables check passed")
    return True

def main():
    """Main startup function."""
    logger.info("Starting LaudatorAI backend...")
    
    # Check environment
    check_environment()
    
    # Import and start the application
    try:
        import uvicorn
        from app.main import app
        
        port = int(os.getenv('PORT', 8000))
        host = os.getenv('HOST', '0.0.0.0')
        
        logger.info(f"Starting server on {host}:{port}")
        logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
        logger.info(f"Debug mode: {os.getenv('DEBUG', 'false')}")
        
        uvicorn.run(
            app,
            host=host,
            port=port,
            workers=1,
            log_level="info",
            access_log=True
        )
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    main()
