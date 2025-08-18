#!/usr/bin/env python3
"""
Script to help set CORS environment variable for Railway deployment.
This script provides the exact value you need to set in Railway dashboard.
"""

def main():
    """Print the CORS environment variable value for Railway."""
    
    cors_origins = [
        "https://laudator-ai.vercel.app",
        "https://laudator-ai-tannercline-5407s-projects.vercel.app",
        "https://laudator-ai-git-main-tannercline-5407s-projects.vercel.app"
    ]
    
    # Format as JSON string for environment variable
    cors_json = '["' + '","'.join(cors_origins) + '"]'
    
    print("=" * 60)
    print("RAILWAY CORS ENVIRONMENT VARIABLE SETUP")
    print("=" * 60)
    print()
    print("Follow these steps to fix the CORS issue:")
    print()
    print("1. Go to your Railway project dashboard")
    print("2. Navigate to your backend service")
    print("3. Go to the 'Variables' tab")
    print("4. Add a new environment variable:")
    print()
    print("   Variable Name: BACKEND_CORS_ORIGINS")
    print("   Variable Value: " + cors_json)
    print()
    print("5. Save the variable")
    print("6. Redeploy your service")
    print()
    print("Alternative: You can also use a comma-separated format:")
    print("   Variable Value: " + ",".join(cors_origins))
    print()
    print("After setting this variable, your frontend should be able")
    print("to communicate with your backend without CORS errors.")
    print("=" * 60)

if __name__ == "__main__":
    main()
