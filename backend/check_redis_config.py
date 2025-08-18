#!/usr/bin/env python3
"""Check Redis configuration and connection in Railway."""

import os
import sys
import logging
from urllib.parse import urlparse

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_redis_environment():
    """Check Redis-related environment variables."""
    logger.info("=== Redis Environment Variables Check ===")
    
    # Check for Redis URL
    redis_url = os.getenv('REDIS_URL')
    if redis_url:
        logger.info(f"✓ REDIS_URL is set")
        
        # Parse the URL to check format
        try:
            parsed = urlparse(redis_url)
            logger.info(f"  - Scheme: {parsed.scheme}")
            logger.info(f"  - Host: {parsed.hostname}")
            logger.info(f"  - Port: {parsed.port}")
            logger.info(f"  - Username: {parsed.username or 'None'}")
            logger.info(f"  - Database: {parsed.path[1:] if parsed.path else '0'}")
            
            # Check if it's a valid Redis URL
            if parsed.scheme not in ['redis', 'rediss']:
                logger.error(f"  ✗ Invalid scheme: {parsed.scheme} (should be 'redis' or 'rediss')")
            else:
                logger.info(f"  ✓ Valid Redis URL format")
                
        except Exception as e:
            logger.error(f"  ✗ Error parsing REDIS_URL: {e}")
    else:
        logger.error("✗ REDIS_URL is not set")
    
    # Check for other Redis-related variables
    redis_vars = [
        'REDIS_HOST',
        'REDIS_PORT', 
        'REDIS_PASSWORD',
        'REDIS_DB',
        'REDIS_TLS'
    ]
    
    for var in redis_vars:
        value = os.getenv(var)
        if value:
            logger.info(f"✓ {var}: {value}")
        else:
            logger.info(f"⚠ {var}: not set (optional)")

def test_redis_connection():
    """Test Redis connection."""
    logger.info("=== Redis Connection Test ===")
    
    redis_url = os.getenv('REDIS_URL')
    if not redis_url:
        logger.error("✗ Cannot test connection: REDIS_URL not set")
        return False
    
    try:
        import redis
        
        logger.info("Attempting to connect to Redis...")
        r = redis.from_url(redis_url)
        
        # Test basic connection
        pong = r.ping()
        logger.info(f"✓ Redis ping successful: {pong}")
        
        # Test basic operations
        test_key = "laudatorai_test_connection"
        test_value = "test_value"
        
        # Set a test value
        r.set(test_key, test_value)
        logger.info(f"✓ Set operation successful")
        
        # Get the test value
        retrieved_value = r.get(test_key)
        if retrieved_value and retrieved_value.decode() == test_value:
            logger.info(f"✓ Get operation successful")
        else:
            logger.error(f"✗ Get operation failed: expected '{test_value}', got '{retrieved_value}'")
            return False
        
        # Delete the test key
        r.delete(test_key)
        logger.info(f"✓ Delete operation successful")
        
        # Test list operations (for Celery)
        r.lpush("test_list", "test_item")
        r.lpop("test_list")
        logger.info(f"✓ List operations successful")
        
        logger.info("✓ All Redis operations successful")
        return True
        
    except redis.ConnectionError as e:
        logger.error(f"✗ Redis connection failed: {e}")
        return False
    except redis.AuthenticationError as e:
        logger.error(f"✗ Redis authentication failed: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ Unexpected Redis error: {e}")
        return False

def check_celery_redis_config():
    """Check if Celery can use Redis as broker."""
    logger.info("=== Celery Redis Configuration Check ===")
    
    try:
        from celery import Celery
        from app.core.config import settings
        
        logger.info(f"Redis URL from settings: {settings.REDIS_URL}")
        
        # Test Celery app creation with Redis
        test_celery = Celery('test_app', broker=settings.REDIS_URL)
        logger.info("✓ Celery app created successfully with Redis broker")
        
        # Test Celery connection
        try:
            test_celery.control.inspect().active()
            logger.info("✓ Celery can connect to Redis broker")
        except Exception as e:
            logger.warning(f"⚠ Celery connection test failed: {e}")
            logger.info("This might be normal if no workers are running")
        
        return True
        
    except ImportError as e:
        logger.error(f"✗ Celery not available: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ Celery Redis configuration failed: {e}")
        return False

def check_railway_redis_service():
    """Check if Redis service is properly configured in Railway."""
    logger.info("=== Railway Redis Service Check ===")
    
    # Check if we're running in Railway
    railway_env = os.getenv('RAILWAY_ENVIRONMENT')
    if railway_env:
        logger.info(f"✓ Running in Railway environment: {railway_env}")
    else:
        logger.info("⚠ Not running in Railway environment")
    
    # Check for Railway-specific Redis variables
    railway_redis_vars = [
        'RAILWAY_REDIS_URL',
        'REDIS_URL',
        'REDISCLOUD_URL'
    ]
    
    for var in railway_redis_vars:
        value = os.getenv(var)
        if value:
            logger.info(f"✓ {var} is set")
        else:
            logger.info(f"⚠ {var} is not set")

def main():
    """Run all Redis configuration checks."""
    logger.info("Starting Redis Configuration Check...")
    
    check_redis_environment()
    check_railway_redis_service()
    
    # Only test connection if we have a Redis URL
    if os.getenv('REDIS_URL'):
        connection_ok = test_redis_connection()
        if connection_ok:
            check_celery_redis_config()
    else:
        logger.warning("Skipping connection tests - no REDIS_URL found")
    
    logger.info("=== Redis Configuration Check Complete ===")

if __name__ == "__main__":
    main()
