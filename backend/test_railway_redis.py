#!/usr/bin/env python3
"""Simple Redis connection test for Railway."""

import os
import sys

def test_redis():
    """Test Redis connection and print results."""
    print("=== Redis Connection Test ===")
    
    # Check environment variables
    redis_url = os.getenv('REDIS_URL')
    if not redis_url:
        print("❌ REDIS_URL is not set")
        print("Please add a Redis service to your Railway project")
        return False
    
    print(f"✅ REDIS_URL is set")
    print(f"URL: {redis_url[:20]}..." if len(redis_url) > 20 else f"URL: {redis_url}")
    
    try:
        import redis
        print("✅ Redis module imported successfully")
        
        # Test connection
        r = redis.from_url(redis_url)
        pong = r.ping()
        print(f"✅ Redis ping successful: {pong}")
        
        # Test basic operations
        test_key = "laudatorai_test"
        test_value = "test_value"
        
        r.set(test_key, test_value)
        retrieved = r.get(test_key)
        r.delete(test_key)
        
        if retrieved and retrieved.decode() == test_value:
            print("✅ Redis read/write operations successful")
        else:
            print("❌ Redis read/write operations failed")
            return False
        
        print("✅ All Redis tests passed!")
        return True
        
    except ImportError:
        print("❌ Redis module not available")
        print("Make sure 'redis' is in your requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_redis()
    sys.exit(0 if success else 1)
