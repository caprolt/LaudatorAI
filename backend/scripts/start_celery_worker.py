#!/usr/bin/env python3
"""Celery worker startup script."""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.core.celery_app import celery_app
from app.core.logging import setup_logging

def main():
    """Start the Celery worker."""
    logger = setup_logging()
    logger.info("Starting Celery worker...")
    
    # Start the worker
    celery_app.worker_main([
        'worker',
        '--loglevel=info',
        '--concurrency=2',
        '--queues=job_processing,resume_processing,application_processing,cleanup'
    ])

if __name__ == "__main__":
    main()
