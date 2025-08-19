#!/usr/bin/env python3
"""Debug script for Railway environment variables and database connection."""

import os
import sys
from urllib.parse import urlparse

def debug_environment():
    """Debug environment variables and database connection."""
    print("=== Railway Environment Debug ===")
    print()
    
    # Check environment variables
    print("Environment Variables:")
    print(f"  PORT: {os.getenv('PORT', 'NOT SET')}")
    print(f"  HOST: {os.getenv('HOST', 'NOT SET')}")
    print(f"  ENVIRONMENT: {os.getenv('ENVIRONMENT', 'NOT SET')}")
    print()
    
    # Check DATABASE_URL
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        print("DATABASE_URL Analysis:")
        try:
            parsed = urlparse(database_url)
            print(f"  Scheme: {parsed.scheme}")
            print(f"  Host: {parsed.hostname}")
            print(f"  Port: {parsed.port}")
            print(f"  Database: {parsed.path[1:] if parsed.path else 'NOT SET'}")
            print(f"  Username: {parsed.username}")
            print(f"  Password: {'***' if parsed.password else 'NOT SET'}")
            
            # Check for Railway internal hostname
            if 'railway.internal' in parsed.hostname:
                print("  ⚠️  WARNING: Internal Railway hostname detected!")
                print("     This URL is only accessible from within Railway's network.")
                print("     Make sure your services are properly linked in Railway dashboard.")
            elif 'railway.app' in parsed.hostname:
                print("  ✅ External Railway hostname detected")
            else:
                print(f"  ℹ️  Custom hostname: {parsed.hostname}")
        except Exception as e:
            print(f"  ❌ Error parsing DATABASE_URL: {e}")
    else:
        print("DATABASE_URL: NOT SET")
        print("  Make sure you have a PostgreSQL service added to your Railway project")
        print("  and it's properly linked to your backend service.")
    print()
    
    # Check REDIS_URL
    redis_url = os.getenv('REDIS_URL')
    if redis_url:
        print("REDIS_URL Analysis:")
        try:
            parsed = urlparse(redis_url)
            print(f"  Scheme: {parsed.scheme}")
            print(f"  Host: {parsed.hostname}")
            print(f"  Port: {parsed.port}")
            print(f"  Database: {parsed.path[1:] if parsed.path else '0'}")
            
            if 'railway.internal' in parsed.hostname:
                print("  ⚠️  WARNING: Internal Railway hostname detected!")
            elif 'railway.app' in parsed.hostname:
                print("  ✅ External Railway hostname detected")
            else:
                print(f"  ℹ️  Custom hostname: {parsed.hostname}")
        except Exception as e:
            print(f"  ❌ Error parsing REDIS_URL: {e}")
    else:
        print("REDIS_URL: NOT SET")
        print("  Make sure you have a Redis service added to your Railway project")
        print("  and it's properly linked to your backend service.")
    print()
    
    # Test database connection
    if database_url:
        print("Database Connection Test:")
        try:
            import psycopg2
            from urllib.parse import urlparse
            
            parsed = urlparse(database_url)
            conn_params = {
                'host': parsed.hostname,
                'port': parsed.port or 5432,
                'database': parsed.path[1:] if parsed.path else 'postgres',
                'user': parsed.username,
                'password': parsed.password
            }
            
            print(f"  Attempting connection to {parsed.hostname}:{parsed.port or 5432}...")
            conn = psycopg2.connect(**conn_params)
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"  ✅ Connection successful!")
            print(f"  PostgreSQL version: {version[0]}")
            cursor.close()
            conn.close()
        except ImportError:
            print("  ❌ psycopg2 not installed. Install with: pip install psycopg2-binary")
        except Exception as e:
            print(f"  ❌ Connection failed: {e}")
            print("  This could be due to:")
            print("    1. Services not properly linked in Railway")
            print("    2. Internal hostname not accessible from current environment")
            print("    3. Database service not running")
            print("    4. Incorrect credentials")
    print()
    
    print("=== Debug Complete ===")
    print()
    print("Next steps:")
    print("1. If you see internal hostnames, make sure services are linked in Railway dashboard")
    print("2. If DATABASE_URL/REDIS_URL are not set, add PostgreSQL and Redis services to your project")
    print("3. If connection fails, check that services are running and properly configured")

if __name__ == "__main__":
    debug_environment()
