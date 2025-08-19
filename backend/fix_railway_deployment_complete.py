#!/usr/bin/env python3
"""Comprehensive Railway deployment fix script."""

import os
import sys
import logging
import subprocess
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def check_railway_cli():
    """Check if Railway CLI is installed."""
    try:
        result = subprocess.run(['railway', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("✓ Railway CLI is installed")
            return True
        else:
            logger.warning("⚠ Railway CLI not found or not working")
            return False
    except FileNotFoundError:
        logger.warning("⚠ Railway CLI not installed")
        return False

def install_railway_cli():
    """Install Railway CLI if not present."""
    logger.info("Installing Railway CLI...")
    try:
        subprocess.run(['npm', 'install', '-g', '@railway/cli'], check=True)
        logger.info("✓ Railway CLI installed successfully")
        return True
    except subprocess.CalledProcessError:
        logger.error("✗ Failed to install Railway CLI")
        return False

def check_git_status():
    """Check if we're in a git repository and if changes are committed."""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        if result.stdout.strip():
            logger.warning("⚠ You have uncommitted changes. Consider committing them before deploying.")
            return False
        else:
            logger.info("✓ Git repository is clean")
            return True
    except subprocess.CalledProcessError:
        logger.warning("⚠ Not in a git repository or git not available")
        return False

def create_railway_project():
    """Create a new Railway project if needed."""
    print_header("RAILWAY PROJECT SETUP")
    
    print("To create a new Railway project:")
    print("1. Go to https://railway.app")
    print("2. Click 'New Project'")
    print("3. Select 'Deploy from GitHub repo'")
    print("4. Choose your repository")
    print("5. Select the 'backend' directory as the source")
    print()
    
    response = input("Have you created the Railway project? (y/n): ").lower().strip()
    if response == 'y':
        logger.info("✓ Railway project created")
        return True
    else:
        logger.warning("Please create the Railway project first")
        return False

def add_required_services():
    """Instructions for adding required services."""
    print_header("ADDING REQUIRED SERVICES")
    
    print("You need to add these services to your Railway project:")
    print()
    print("1. POSTGRESQL DATABASE:")
    print("   - Go to your Railway project dashboard")
    print("   - Click 'New Service'")
    print("   - Select 'Database' → 'PostgreSQL'")
    print("   - This will automatically provide DATABASE_URL")
    print()
    print("2. REDIS SERVICE:")
    print("   - Click 'New Service' again")
    print("   - Select 'Database' → 'Redis'")
    print("   - This will automatically provide REDIS_URL")
    print()
    
    response = input("Have you added PostgreSQL and Redis services? (y/n): ").lower().strip()
    if response == 'y':
        logger.info("✓ Required services added")
        return True
    else:
        logger.warning("Please add PostgreSQL and Redis services first")
        return False

def set_environment_variables():
    """Instructions for setting environment variables."""
    print_header("SETTING ENVIRONMENT VARIABLES")
    
    print("In your Railway backend service, go to 'Variables' tab and add:")
    print()
    print("Required variables:")
    print("BACKEND_CORS_ORIGINS=https://your-frontend-domain.vercel.app,http://localhost:3000")
    print("ENVIRONMENT=production")
    print("DEBUG=false")
    print()
    print("Optional variables:")
    print("OPENAI_API_KEY=your-openai-api-key")
    print("MINIO_ENDPOINT=your-minio-endpoint")
    print("MINIO_ACCESS_KEY=your-minio-access-key")
    print("MINIO_SECRET_KEY=your-minio-secret-key")
    print()
    
    response = input("Have you set the environment variables? (y/n): ").lower().strip()
    if response == 'y':
        logger.info("✓ Environment variables set")
        return True
    else:
        logger.warning("Please set the environment variables first")
        return False

def configure_dependencies():
    """Instructions for configuring service dependencies."""
    print_header("CONFIGURING SERVICE DEPENDENCIES")
    
    print("Configure service dependencies:")
    print("1. Go to your backend service")
    print("2. Click 'Settings' → 'Dependencies'")
    print("3. Add dependencies on:")
    print("   - PostgreSQL service")
    print("   - Redis service")
    print("4. This ensures services start in the correct order")
    print()
    
    response = input("Have you configured service dependencies? (y/n): ").lower().strip()
    if response == 'y':
        logger.info("✓ Service dependencies configured")
        return True
    else:
        logger.warning("Please configure service dependencies first")
        return False

def test_deployment():
    """Test the deployment."""
    print_header("TESTING DEPLOYMENT")
    
    print("To test your deployment:")
    print("1. Check Railway logs for any errors")
    print("2. Test health endpoint: https://your-app.railway.app/health")
    print("3. Test API docs: https://your-app.railway.app/docs")
    print("4. Run the debug script: railway run python debug_railway.py")
    print()
    
    response = input("Would you like to test the deployment now? (y/n): ").lower().strip()
    if response == 'y':
        logger.info("Running deployment test...")
        return True
    else:
        logger.info("Skipping deployment test")
        return False

def run_debug_script():
    """Run the debug script to verify the deployment."""
    try:
        logger.info("Running debug script...")
        result = subprocess.run(['python', 'debug_railway.py'], 
                              capture_output=True, text=True, cwd='.')
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        logger.error(f"Failed to run debug script: {e}")
        return False

def main():
    """Main function to fix Railway deployment."""
    print_header("RAILWAY DEPLOYMENT FIX SCRIPT")
    
    logger.info("This script will help you fix your Railway deployment issues.")
    logger.info("Follow the instructions step by step.")
    
    # Check Railway CLI
    if not check_railway_cli():
        install_railway_cli()
    
    # Check git status
    check_git_status()
    
    # Step 1: Create Railway project
    if not create_railway_project():
        return
    
    # Step 2: Add required services
    if not add_required_services():
        return
    
    # Step 3: Set environment variables
    if not set_environment_variables():
        return
    
    # Step 4: Configure dependencies
    if not configure_dependencies():
        return
    
    # Step 5: Test deployment
    if test_deployment():
        run_debug_script()
    
    print_header("DEPLOYMENT FIX COMPLETE")
    print("Your Railway deployment should now be working!")
    print()
    print("Next steps:")
    print("1. Push your code to trigger a new deployment")
    print("2. Monitor the deployment logs")
    print("3. Test your API endpoints")
    print("4. Update your frontend to use the new backend URL")
    print()
    print("If you encounter any issues:")
    print("1. Check Railway logs")
    print("2. Run: railway run python debug_railway.py")
    print("3. Verify all environment variables are set")
    print("4. Ensure all services are running")

if __name__ == "__main__":
    main()
