"""Job description processing endpoints."""

import json
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import HttpUrl, ValidationError

from app.core.database import get_db
from app.schemas import JobCreate, JobResponse, JobUpdate, JobUrlRequest, JobProcessingResponse
from app.models import Job
from app.services.job_processing import process_job_posting
from app.services.web_scraping import scrape_job_posting
from app.services.jd_normalization import normalize_job_description

router = APIRouter()


@router.post("/", response_model=JobResponse)
async def create_job(job: JobCreate, db: Session = Depends(get_db)):
    """Create a new job posting."""
    try:
        # Validate URL
        if not str(job.url).startswith(('http://', 'https://')):
            raise HTTPException(status_code=400, detail="Invalid URL format")
        
        # Check if job already exists
        existing_job = db.query(Job).filter(Job.url == str(job.url)).first()
        if existing_job:
            raise HTTPException(status_code=409, detail="Job posting already exists")
        
        # Create job record
        db_job = Job(
            url=str(job.url),
            title=job.title or "Processing...",
            company=job.company or "Processing...",
            location=job.location,
            description=job.description or "Processing...",
            requirements=job.requirements,
            status="pending"
        )
        
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        
        # Start background processing
        process_job_posting.delay(db_job.id, str(job.url))
        
        return db_job
        
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create job: {str(e)}")


@router.get("/", response_model=List[JobResponse])
async def list_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all jobs."""
    jobs = db.query(Job).offset(skip).limit(limit).all()
    return jobs


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get job by ID."""
    job = db.query(Job).filter(Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.put("/{job_id}", response_model=JobResponse)
async def update_job(job_id: int, job_update: JobUpdate, db: Session = Depends(get_db)):
    """Update job by ID."""
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Update fields
    update_data = job_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_job, field, value)
    
    db.commit()
    db.refresh(db_job)
    return db_job


@router.delete("/{job_id}")
async def delete_job(job_id: int, db: Session = Depends(get_db)):
    """Delete job by ID."""
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db.delete(db_job)
    db.commit()
    return {"message": "Job deleted successfully"}


@router.post("/process-url", response_model=JobProcessingResponse)
async def process_job_url(request: JobUrlRequest, db: Session = Depends(get_db)):
    """Process a job posting URL directly and return normalized content."""
    try:
        url = str(request.url)
        
        # Check if job already exists
        existing_job = db.query(Job).filter(Job.url == url).first()
        if existing_job:
            # Return existing job if already processed
            if existing_job.status == "completed":
                return {
                    "job_id": existing_job.id,
                    "status": "completed",
                    "title": existing_job.title,
                    "company": existing_job.company,
                    "location": existing_job.location,
                    "description": existing_job.description,
                    "requirements": existing_job.requirements,
                    "normalized_content": json.loads(existing_job.normalized_content) if existing_job.normalized_content else None
                }
            else:
                raise HTTPException(status_code=409, detail="Job is already being processed")
        
        # Create job record
        db_job = Job(
            url=url,
            title="Processing...",
            company="Processing...",
            description="Processing...",
            status="pending"
        )
        
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        
        # Start background processing
        process_job_posting.delay(db_job.id, url)
        
        return {
            "job_id": db_job.id,
            "status": "processing",
            "message": "Job processing started"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to process job URL: {str(e)}")


@router.get("/{job_id}/status")
async def get_job_status(job_id: int, db: Session = Depends(get_db)):
    """Get job processing status."""
    job = db.query(Job).filter(Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    response = {
        "job_id": job.id,
        "status": job.status,
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "created_at": job.created_at,
        "updated_at": job.updated_at
    }
    
    if job.status == "completed" and job.normalized_content:
        try:
            response["normalized_content"] = json.loads(job.normalized_content)
        except json.JSONDecodeError:
            response["normalized_content"] = None
    
    return response
