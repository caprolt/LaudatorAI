"""Job processing service with Celery tasks."""

import time
import asyncio
from typing import Dict, Any
from sqlalchemy.orm import Session

from app.core.celery_app import celery_app
from app.core.logging import log_task_start, log_task_complete, log_task_error
from app.core.database import get_db
from app.models import Job
from app.services.web_scraping import scrape_job_posting
from app.services.jd_normalization import normalize_job_description


@celery_app.task(bind=True)
def process_job_posting(self, job_id: int, url: str) -> Dict[str, Any]:
    """Process a job posting URL and extract job details."""
    task_id = self.request.id
    task_type = "job_processing"
    start_time = time.time()
    
    try:
        log_task_start(task_id, task_type, job_id=job_id, url=url)
        
        # Get database session
        db = next(get_db())
        
        # Update job status to processing
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise ValueError(f"Job with ID {job_id} not found")
        
        job.status = "processing"
        db.commit()
        
        # Scrape the job posting
        raw_content = asyncio.run(scrape_job_posting(url))
        
        # Normalize the job description
        normalized = normalize_job_description(raw_content)
        
        # Update job with scraped and normalized content
        job.title = normalized.title or job.title
        job.company = normalized.company or job.company
        job.location = normalized.location or job.location
        job.description = normalized.description or job.description
        job.requirements = "\n".join(normalized.requirements) if normalized.requirements else None
        job.raw_content = normalized.raw_content
        job.normalized_content = _serialize_normalized_content(normalized)
        job.status = "completed"
        
        db.commit()
        
        result = {
            "job_id": job_id,
            "status": "completed",
            "title": normalized.title,
            "company": normalized.company,
            "requirements_count": len(normalized.requirements),
            "skills_count": len(normalized.skills)
        }
        
        duration = time.time() - start_time
        log_task_complete(task_id, task_type, duration=duration, job_id=job_id)
        
        return result
        
    except Exception as e:
        duration = time.time() - start_time
        
        # Update job status to failed
        try:
            db = next(get_db())
            job = db.query(Job).filter(Job.id == job_id).first()
            if job:
                job.status = "failed"
                db.commit()
        except Exception:
            pass
        
        log_task_error(task_id, task_type, str(e), job_id=job_id, duration=duration)
        raise


@celery_app.task(bind=True)
def normalize_job_description(self, job_id: int, raw_content: str) -> Dict[str, Any]:
    """Normalize and structure job description content."""
    task_id = self.request.id
    task_type = "job_normalization"
    start_time = time.time()
    
    try:
        log_task_start(task_id, task_type, job_id=job_id)
        
        # Get database session
        db = next(get_db())
        
        # Get job record
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise ValueError(f"Job with ID {job_id} not found")
        
        # Parse raw content if it's a string
        if isinstance(raw_content, str):
            import json
            raw_content = json.loads(raw_content)
        
        # Normalize the job description
        normalized = normalize_job_description(raw_content)
        
        # Update job with normalized content
        job.normalized_content = _serialize_normalized_content(normalized)
        job.status = "completed"
        
        db.commit()
        
        result = {
            "job_id": job_id,
            "status": "normalized",
            "requirements_count": len(normalized.requirements),
            "skills_count": len(normalized.skills)
        }
        
        duration = time.time() - start_time
        log_task_complete(task_id, task_type, duration=duration, job_id=job_id)
        
        return result
        
    except Exception as e:
        duration = time.time() - start_time
        log_task_error(task_id, task_type, str(e), job_id=job_id, duration=duration)
        raise


def _serialize_normalized_content(normalized) -> str:
    """Serialize normalized content to JSON string."""
    import json
    
    return json.dumps({
        "title": normalized.title,
        "company": normalized.company,
        "location": normalized.location,
        "description": normalized.description,
        "requirements": normalized.requirements,
        "responsibilities": normalized.responsibilities,
        "benefits": normalized.benefits,
        "salary_range": normalized.salary_range,
        "employment_type": normalized.employment_type,
        "experience_level": normalized.experience_level,
        "skills": normalized.skills,
        "education": normalized.education,
        "industry": normalized.industry,
        "department": normalized.department
    })
