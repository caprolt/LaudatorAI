"""Application processing service with Celery tasks."""

import time
from typing import Dict, Any

from app.core.celery_app import celery_app
from app.core.logging import log_task_start, log_task_complete, log_task_error
from app.services.resume_processing import tailor_resume
from app.services.cover_letter_processing import generate_cover_letter


@celery_app.task(bind=True)
def process_application(self, application_id: int, job_id: int, resume_id: int) -> Dict[str, Any]:
    """Process a complete job application (resume + cover letter)."""
    task_id = self.request.id
    task_type = "application_processing"
    
    try:
        log_task_start(task_id, task_type, application_id=application_id, job_id=job_id, resume_id=resume_id)
        start_time = time.time()
        
        # Start resume tailoring
        tailor_task = tailor_resume.delay(application_id, job_id, resume_id)
        
        # Start cover letter generation
        cover_letter_task = generate_cover_letter.delay(application_id, job_id, resume_id)
        
        result = {
            "application_id": application_id,
            "job_id": job_id,
            "resume_id": resume_id,
            "tailor_task_id": tailor_task.id,
            "cover_letter_task_id": cover_letter_task.id,
            "status": "processing",
            "message": "Application processing started - resume tailoring and cover letter generation initiated"
        }
        
        duration = time.time() - start_time
        log_task_complete(task_id, task_type, duration=duration, application_id=application_id)
        
        return result
        
    except Exception as e:
        duration = time.time() - start_time
        log_task_error(task_id, task_type, str(e), application_id=application_id, duration=duration)
        raise



