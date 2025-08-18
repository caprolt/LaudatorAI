#!/usr/bin/env python3
"""Fix Redis connection issues in Railway."""

import os
import sys
import socket

def check_redis_hostname():
    """Check if we can resolve the Redis hostname."""
    print("=== Redis Hostname Resolution Check ===")
    
    redis_url = os.getenv('REDIS_URL')
    if not redis_url:
        print("❌ REDIS_URL is not set")
        return False
    
    # Extract hostname from Redis URL
    try:
        # Simple parsing - look for the hostname part
        if 'redis.railway.internal' in redis_url:
            hostname = 'redis.railway.internal'
        elif 'redis://' in redis_url:
            # Extract hostname from redis://hostname:port format
            parts = redis_url.replace('redis://', '').split('/')[0]
            hostname = parts.split(':')[0]
        else:
            print(f"❌ Could not parse hostname from: {redis_url}")
            return False
        
        print(f"Hostname to test: {hostname}")
        
        # Try to resolve the hostname
        try:
            ip = socket.gethostbyname(hostname)
            print(f"✅ Hostname resolved to IP: {ip}")
            return True
        except socket.gaierror as e:
            print(f"❌ Could not resolve hostname '{hostname}': {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error parsing Redis URL: {e}")
        return False

def suggest_fixes():
    """Suggest fixes for Redis connection issues."""
    print("\n=== Suggested Fixes ===")
    
    print("1. **Check Service Dependencies in Railway:**")
    print("   - Go to your Railway dashboard")
    print("   - Click on your backend service")
    print("   - Go to 'Settings' tab")
    print("   - Look for 'Service Dependencies' or 'Connected Services'")
    print("   - Make sure Redis service is listed as a dependency")
    
    print("\n2. **Reconnect Services:**")
    print("   - In backend service settings, look for 'Connect to Service'")
    print("   - Select your Redis service")
    print("   - Railway will update REDIS_URL automatically")
    
    print("\n3. **Check Service Status:**")
    print("   - Ensure both backend and Redis services are running")
    print("   - Check that they're in the same Railway project")
    
    print("\n4. **Alternative: Use External Redis URL:**")
    print("   - Go to your Redis service in Railway")
    print("   - Look for 'Connect' or 'External URL'")
    print("   - Use the external URL instead of internal")
    
    print("\n5. **Manual Environment Variable Fix:**")
    print("   - Go to backend service Variables tab")
    print("   - Look for the correct Redis URL format")
    print("   - It should be something like: redis://default:password@hostname:port")

def test_alternative_redis_urls():
    """Test alternative Redis URL formats."""
    print("\n=== Testing Alternative Redis URLs ===")
    
    # Common Railway Redis URL patterns
    test_urls = [
        os.getenv('REDIS_URL'),
        os.getenv('REDISCLOUD_URL'),
        os.getenv('RAILWAY_REDIS_URL'),
    ]
    
    for i, url in enumerate(test_urls):
        if url:
            print(f"Test URL {i+1}: {url[:30]}...")
            try:
                import redis
                r = redis.from_url(url)
                pong = r.ping()
                print(f"✅ URL {i+1} works! Ping: {pong}")
                return url
            except Exception as e:
                print(f"❌ URL {i+1} failed: {e}")
    
    return None

def main():
    """Main function to diagnose and fix Redis issues."""
    print("=== Railway Redis Connection Fix ===")
    
    # Check hostname resolution
    hostname_ok = check_redis_hostname()
    
    # Test alternative URLs
    working_url = test_alternative_redis_urls()
    
    # Suggest fixes
    suggest_fixes()
    
    if working_url:
        print(f"\n✅ Found working Redis URL: {working_url[:30]}...")
        print("You can use this URL in your environment variables.")
    elif not hostname_ok:
        print("\n❌ Hostname resolution failed. This indicates a service connection issue.")
        print("Please follow the suggested fixes above.")
    else:
        print("\n⚠️ Hostname resolves but connection fails. Check service dependencies.")

if __name__ == "__main__":
    main()
