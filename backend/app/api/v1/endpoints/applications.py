"""Job application endpoints."""

from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import JobApplicationCreate, JobApplicationResponse, JobApplicationUpdate
from app.models import JobApplication, Job, Resume
from app.services.application_processing import process_application, generate_cover_letter

router = APIRouter()


@router.post("/", response_model=JobApplicationResponse)
async def create_application(application: JobApplicationCreate, db: Session = Depends(get_db)):
    """Create a new job application."""
    # Verify job exists
    job = db.query(Job).filter(Job.id == application.job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Verify resume exists
    resume = db.query(Resume).filter(Resume.id == application.resume_id).first()
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Create application record
    db_application = JobApplication(
        job_id=application.job_id,
        resume_id=application.resume_id
    )
    
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    
    # Start background processing
    process_application.delay(db_application.id, application.job_id, application.resume_id)
    
    return db_application


@router.get("/", response_model=List[JobApplicationResponse])
async def list_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all job applications."""
    applications = db.query(JobApplication).offset(skip).limit(limit).all()
    return applications


@router.get("/{application_id}", response_model=JobApplicationResponse)
async def get_application(application_id: int, db: Session = Depends(get_db)):
    """Get job application by ID."""
    application = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if application is None:
        raise HTTPException(status_code=404, detail="Job application not found")
    return application


@router.put("/{application_id}", response_model=JobApplicationResponse)
async def update_application(application_id: int, application_update: JobApplicationUpdate, db: Session = Depends(get_db)):
    """Update job application by ID."""
    db_application = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if db_application is None:
        raise HTTPException(status_code=404, detail="Job application not found")
    
    # Update fields
    update_data = application_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_application, field, value)
    
    db.commit()
    db.refresh(db_application)
    return db_application


@router.delete("/{application_id}")
async def delete_application(application_id: int, db: Session = Depends(get_db)):
    """Delete job application by ID."""
    db_application = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if db_application is None:
        raise HTTPException(status_code=404, detail="Job application not found")
    
    db.delete(db_application)
    db.commit()
    return {"message": "Job application deleted successfully"}


@router.post("/{application_id}/generate-cover-letter")
async def generate_cover_letter_for_application(application_id: int, db: Session = Depends(get_db)):
    """Generate a cover letter for a job application."""
    db_application = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if db_application is None:
        raise HTTPException(status_code=404, detail="Job application not found")
    
    # Start background cover letter generation
    generate_cover_letter.delay(application_id, db_application.job_id, db_application.resume_id)
    
    return {"message": "Cover letter generation started", "application_id": application_id}
