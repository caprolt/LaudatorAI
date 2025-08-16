"""Job description processing endpoints."""

from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import JobCreate, JobResponse, JobUpdate
from app.models import Job
from app.services.job_processing import process_job_posting

router = APIRouter()


@router.post("/", response_model=JobResponse)
async def create_job(job: JobCreate, db: Session = Depends(get_db)):
    """Create a new job posting."""
    # Create job record
    db_job = Job(
        url=str(job.url),
        title=job.title,
        company=job.company,
        location=job.location,
        description=job.description,
        requirements=job.requirements
    )
    
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    
    # Start background processing
    process_job_posting.delay(db_job.id, str(job.url))
    
    return db_job


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
