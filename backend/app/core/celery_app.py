"""Celery application configuration."""

from celery import Celery
from app.core.config import settings

# Create Celery instance
celery_app = Celery(
    "laudatorai",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.services.job_processing",
        "app.services.resume_processing",
        "app.services.application_processing"
    ]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    result_expires=3600,  # 1 hour
    beat_schedule={
        "cleanup-old-tasks": {
            "task": "app.services.cleanup.cleanup_old_tasks",
            "schedule": 3600.0,  # Every hour
        },
        "cleanup-stuck-jobs": {
            "task": "app.services.cleanup.cleanup_stuck_jobs",
            "schedule": 900.0,  # Every 15 minutes
        },
    },
)

# Task routing
celery_app.conf.task_routes = {
    "app.services.job_processing.*": {"queue": "job_processing"},
    "app.services.resume_processing.*": {"queue": "resume_processing"},
    "app.services.application_processing.*": {"queue": "application_processing"},
    "app.services.cleanup.*": {"queue": "cleanup"},
}
