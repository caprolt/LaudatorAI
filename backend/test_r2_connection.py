#!/usr/bin/env python3
"""Test script to verify Cloudflare R2 connectivity."""

import os
import tempfile
from pathlib import Path

# Add the app directory to the Python path
import sys
sys.path.append(str(Path(__file__).parent))

from app.core.config import settings
from app.services.file_storage import get_file_storage


def test_r2_connection():
    """Test R2 connectivity and basic operations."""
    print("🔍 Testing Cloudflare R2 Connection...")
    
    # Check configuration
    print(f"Storage Type: {settings.file_storage_type}")
    print(f"Bucket Name: {settings.S3_BUCKET_NAME}")
    print(f"Endpoint URL: {settings.S3_ENDPOINT_URL}")
    print(f"Region: {settings.AWS_REGION}")
    
    if not settings.AWS_ACCESS_KEY_ID or not settings.AWS_SECRET_ACCESS_KEY:
        print("❌ AWS credentials not found!")
        print("Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.")
        return False
    
    try:
        # Initialize file storage
        file_storage = get_file_storage()
        print("✅ File storage service initialized successfully")
        
        # Test bucket access
        print("🔍 Testing bucket access...")
        files = file_storage.list_files()
        print(f"✅ Bucket accessible. Found {len(files)} existing files")
        
        # Test file upload
        print("🔍 Testing file upload...")
        test_content = "Hello from LaudatorAI R2 test!"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write(test_content)
            temp_file_path = temp_file.name
        
        try:
            # Upload test file
            object_name = "test/connection_test.txt"
            file_path = file_storage.upload_file(temp_file_path, object_name)
            print(f"✅ File uploaded successfully: {file_path}")
            
            # Test file existence
            if file_storage.file_exists(object_name):
                print("✅ File existence check passed")
            else:
                print("❌ File existence check failed")
                return False
            
            # Test file info
            file_info = file_storage.get_file_info(object_name)
            print(f"✅ File info retrieved: {file_info['size']} bytes")
            
            # Test presigned URL
            presigned_url = file_storage.get_file_url(object_name, expires=3600)
            print(f"✅ Presigned URL generated: {presigned_url[:50]}...")
            
            # Test file download
            download_path = temp_file_path + ".downloaded"
            if file_storage.download_file(object_name, download_path):
                print("✅ File download test passed")
                
                # Verify content
                with open(download_path, 'r') as f:
                    downloaded_content = f.read()
                if downloaded_content == test_content:
                    print("✅ Content verification passed")
                else:
                    print("❌ Content verification failed")
                    return False
            else:
                print("❌ File download test failed")
                return False
            
            # Clean up downloaded file
            os.unlink(download_path)
            
            # Test file deletion
            if file_storage.delete_file(object_name):
                print("✅ File deletion test passed")
            else:
                print("❌ File deletion test failed")
                return False
            
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
        
        print("\n🎉 All R2 tests passed! Your Cloudflare R2 configuration is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ R2 test failed: {e}")
        return False


if __name__ == "__main__":
    success = test_r2_connection()
    sys.exit(0 if success else 1)
