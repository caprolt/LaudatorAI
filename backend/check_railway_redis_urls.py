#!/usr/bin/env python3
"""Check all available Redis URLs in Railway."""

import os
import sys

def check_all_redis_variables():
    """Check all Redis-related environment variables."""
    print("=== All Redis Environment Variables ===")
    
    redis_vars = [
        'REDIS_URL',
        'REDISCLOUD_URL', 
        'RAILWAY_REDIS_URL',
        'REDIS_HOST',
        'REDIS_PORT',
        'REDIS_PASSWORD',
        'REDIS_DB'
    ]
    
    found_vars = {}
    for var in redis_vars:
        value = os.getenv(var)
        if value:
            found_vars[var] = value
            # Mask sensitive parts
            if 'password' in var.lower() or 'key' in var.lower():
                masked = value[:10] + "..." if len(value) > 10 else "***"
                print(f"✅ {var}: {masked}")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: not set")
    
    return found_vars

def test_redis_urls():
    """Test all available Redis URLs."""
    print("\n=== Testing Redis URLs ===")
    
    redis_vars = check_all_redis_variables()
    
    working_url = None
    for var_name, url in redis_vars.items():
        if 'URL' in var_name and url:
            print(f"\nTesting {var_name}: {url[:30]}...")
            try:
                import redis
                r = redis.from_url(url)
                pong = r.ping()
                print(f"✅ {var_name} WORKS! Ping: {pong}")
                working_url = url
                break
            except Exception as e:
                print(f"❌ {var_name} failed: {e}")
    
    return working_url

def suggest_external_url():
    """Suggest how to get external Redis URL."""
    print("\n=== How to Get External Redis URL ===")
    print("1. Go to your Railway dashboard")
    print("2. Click on your Redis service")
    print("3. Look for 'Connect' tab or 'External URL'")
    print("4. Copy the external URL (should look like: redis://default:password@hostname.railway.app:port)")
    print("5. Go to your backend service → Variables tab")
    print("6. Update REDIS_URL with the external URL")

def main():
    """Main function."""
    print("=== Railway Redis URL Checker ===")
    
    working_url = test_redis_urls()
    
    if working_url:
        print(f"\n🎉 SUCCESS! Found working Redis URL: {working_url[:30]}...")
        print("Your Redis connection should work with this URL.")
    else:
        print("\n❌ No working Redis URLs found.")
        suggest_external_url()
        print("\nThe issue is likely that you need to use the external Redis URL instead of the internal one.")

if __name__ == "__main__":
    main()
