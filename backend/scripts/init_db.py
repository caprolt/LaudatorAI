#!/usr/bin/env python3
"""Database initialization script."""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.core.database import init_db
from app.core.logging import setup_logging

def main():
    """Initialize the database."""
    logger = setup_logging()
    
    try:
        logger.info("Initializing database...")
        init_db()
        logger.info("Database initialized successfully!")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
