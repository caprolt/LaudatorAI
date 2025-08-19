#!/usr/bin/env python3
"""Script to set up Railway environment variables and diagnose deployment issues."""

import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_and_set_defaults():
    """Check environment variables and set defaults where appropriate."""
    logger.info("=== Railway Environment Setup ===")
    
    # Check and set PORT (Railway requirement)
    if not os.getenv('PORT'):
        logger.warning("PORT not set, setting default to 8000")
        os.environ['PORT'] = '8000'
    else:
        logger.info(f"✓ PORT: {os.getenv('PORT')}")
    
    # Check and set HOST (Railway requirement)
    if not os.getenv('HOST'):
        logger.warning("HOST not set, setting default to 0.0.0.0")
        os.environ['HOST'] = '0.0.0.0'
    else:
        logger.info(f"✓ HOST: {os.getenv('HOST')}")
    
    # Check and set ENVIRONMENT
    if not os.getenv('ENVIRONMENT'):
        logger.warning("ENVIRONMENT not set, setting default to production")
        os.environ['ENVIRONMENT'] = 'production'
    else:
        logger.info(f"✓ ENVIRONMENT: {os.getenv('ENVIRONMENT')}")
    
    # Check DATABASE_URL
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        logger.info(f"✓ DATABASE_URL: {database_url[:50]}...")
    else:
        logger.error("✗ DATABASE_URL: NOT SET - Add PostgreSQL service to Railway project")
    
    # Check REDIS_URL
    redis_url = os.getenv('REDIS_URL')
    if redis_url:
        logger.info(f"✓ REDIS_URL: {redis_url[:50]}...")
    else:
        logger.error("✗ REDIS_URL: NOT SET - Add Redis service to Railway project")
    
    # Check optional variables
    optional_vars = [
        'BACKEND_CORS_ORIGINS',
        'OPENAI_API_KEY',
        'MINIO_ENDPOINT',
        'MINIO_ACCESS_KEY',
        'MINIO_SECRET_KEY'
    ]
    
    for var in optional_vars:
        if os.getenv(var):
            logger.info(f"✓ {var}: Set")
        else:
            logger.warning(f"⚠ {var}: NOT SET (Optional)")

def test_redis_connection():
    """Test Redis connection with better error handling."""
    logger.info("=== Redis Connection Test ===")
    
    redis_url = os.getenv('REDIS_URL')
    if not redis_url:
        logger.warning("REDIS_URL not set, skipping Redis test")
        return False
    
    try:
        import redis
        logger.info("Attempting to connect to Redis...")
        
        # Parse Redis URL to get connection details
        if redis_url.startswith('redis://'):
            # Remove redis:// prefix for logging
            clean_url = redis_url.replace('redis://', '')
            logger.info(f"Connecting to Redis at: {clean_url}")
        
        r = redis.from_url(redis_url, socket_connect_timeout=5, socket_timeout=5)
        r.ping()
        logger.info("✓ Redis connection successful")
        return True
    except redis.ConnectionError as e:
        logger.error(f"✗ Redis connection failed: {e}")
        logger.error("This might be due to:")
        logger.error("1. Redis service not running in Railway")
        logger.error("2. Network connectivity issues")
        logger.error("3. Incorrect Redis URL format")
        return False
    except Exception as e:
        logger.error(f"✗ Unexpected Redis error: {e}")
        return False

def generate_railway_instructions():
    """Generate instructions for fixing Railway deployment."""
    logger.info("=== Railway Setup Instructions ===")
    
    print("\n" + "="*60)
    print("RAILWAY DEPLOYMENT FIX INSTRUCTIONS")
    print("="*60)
    
    print("\n1. ADD REQUIRED SERVICES TO RAILWAY PROJECT:")
    print("   - Go to your Railway project dashboard")
    print("   - Click 'New Service' → 'Database' → 'PostgreSQL'")
    print("   - Click 'New Service' → 'Database' → 'Redis'")
    print("   - These will automatically provide DATABASE_URL and REDIS_URL")
    
    print("\n2. SET ENVIRONMENT VARIABLES IN RAILWAY:")
    print("   - Go to your backend service → 'Variables' tab")
    print("   - Add these variables:")
    print("     BACKEND_CORS_ORIGINS=https://your-frontend-domain.vercel.app,http://localhost:3000")
    print("     ENVIRONMENT=production")
    print("     DEBUG=false")
    print("     OPENAI_API_KEY=your-openai-api-key (optional)")
    
    print("\n3. CONFIGURE SERVICE DEPENDENCIES:")
    print("   - Go to your backend service → 'Settings' → 'Dependencies'")
    print("   - Add dependencies on PostgreSQL and Redis services")
    
    print("\n4. REDEPLOY:")
    print("   - Railway will automatically redeploy when you push changes")
    print("   - Or manually trigger a redeploy from the dashboard")
    
    print("\n5. VERIFY DEPLOYMENT:")
    print("   - Check Railway logs for any errors")
    print("   - Test health endpoint: https://your-app.railway.app/health")
    print("   - Test API docs: https://your-app.railway.app/docs")

def main():
    """Main function to set up Railway environment."""
    logger.info("Starting Railway Environment Setup...")
    
    # Check and set default environment variables
    check_and_set_defaults()
    
    # Test Redis connection
    redis_ok = test_redis_connection()
    
    # Generate instructions
    generate_railway_instructions()
    
    # Summary
    logger.info("=== Setup Summary ===")
    if redis_ok:
        logger.info("✓ Redis connection test passed")
    else:
        logger.warning("⚠ Redis connection test failed - check Railway services")
    
    logger.info("Environment setup complete. Follow the instructions above to fix Railway deployment.")

if __name__ == "__main__":
    main()
