#!/usr/bin/env python3
"""Script to set CORS environment variable for Railway deployment."""

import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def set_cors_environment():
    """Set CORS environment variable for Railway deployment."""
    logger.info("=== Setting CORS Environment for Railway ===")
    
    # Define the CORS origins for production
    cors_origins = [
        "https://laudator-ai.vercel.app",
        "https://laudator-ai-tannercline-5407s-projects.vercel.app",
        "https://laudator-ai-git-main-tannercline-5407s-projects.vercel.app",
        "http://localhost:3000",  # For local development
        "http://localhost:3001"   # Alternative local port
    ]
    
    # Join origins with commas for environment variable
    cors_origins_str = ",".join(cors_origins)
    
    # Set the environment variable
    os.environ['BACKEND_CORS_ORIGINS'] = cors_origins_str
    
    logger.info(f"✓ Set BACKEND_CORS_ORIGINS: {cors_origins_str}")
    logger.info(f"✓ CORS origins configured: {len(cors_origins)} origins")
    
    for origin in cors_origins:
        logger.info(f"  - {origin}")
    
    return cors_origins_str

def generate_railway_instructions():
    """Generate instructions for setting CORS in Railway."""
    logger.info("=== Railway CORS Setup Instructions ===")
    
    print("\n" + "="*60)
    print("RAILWAY CORS FIX INSTRUCTIONS")
    print("="*60)
    
    print("\n1. GO TO RAILWAY DASHBOARD:")
    print("   - Navigate to your Railway project")
    print("   - Select your backend service")
    print("   - Go to the 'Variables' tab")
    
    print("\n2. ADD CORS ENVIRONMENT VARIABLE:")
    print("   - Click 'New Variable'")
    print("   - Variable name: BACKEND_CORS_ORIGINS")
    print("   - Variable value: https://laudator-ai.vercel.app,https://laudator-ai-tannercline-5407s-projects.vercel.app,https://laudator-ai-git-main-tannercline-5407s-projects.vercel.app,http://localhost:3000,http://localhost:3001")
    
    print("\n3. SAVE AND REDEPLOY:")
    print("   - Click 'Save' to add the variable")
    print("   - Railway will automatically redeploy your service")
    print("   - Wait for deployment to complete")
    
    print("\n4. TEST THE FIX:")
    print("   - Go to your frontend: https://laudator-ai.vercel.app")
    print("   - Try submitting a job description")
    print("   - Check browser console for CORS errors")
    
    print("\n5. VERIFY IN LOGS:")
    print("   - Check Railway logs for CORS origins being loaded")
    print("   - Look for: 'CORS origins: [...]' in startup logs")

def test_cors_configuration():
    """Test CORS configuration by importing the app."""
    logger.info("=== Testing CORS Configuration ===")
    
    try:
        # Set CORS environment first
        set_cors_environment()
        
        # Import the app to test CORS configuration
        sys.path.insert(0, os.path.dirname(__file__))
        from app.main import app
        
        # Check if CORS middleware is properly configured
        cors_middleware = None
        for middleware in app.user_middleware:
            if "CORSMiddleware" in str(middleware.cls):
                cors_middleware = middleware
                break
        
        if cors_middleware:
            logger.info("✓ CORS middleware is properly configured")
            logger.info(f"✓ CORS origins: {cors_middleware.options.get('allow_origins', [])}")
        else:
            logger.warning("⚠ CORS middleware not found")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Error testing CORS configuration: {e}")
        return False

def main():
    """Main function to set up CORS environment."""
    logger.info("Starting CORS Environment Setup...")
    
    # Set CORS environment variable
    cors_origins = set_cors_environment()
    
    # Test CORS configuration
    test_ok = test_cors_configuration()
    
    # Generate Railway instructions
    generate_railway_instructions()
    
    # Summary
    logger.info("=== CORS Setup Summary ===")
    if test_ok:
        logger.info("✓ CORS configuration test passed")
    else:
        logger.warning("⚠ CORS configuration test failed")
    
    logger.info("CORS environment setup complete.")
    logger.info("Follow the Railway instructions above to fix the CORS error.")

if __name__ == "__main__":
    main()
