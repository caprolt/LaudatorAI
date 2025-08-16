"""Job application endpoints."""

from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import JobApplicationCreate, JobApplicationResponse, JobApplicationUpdate
from app.models import JobApplication, Job, Resume
from app.services.application_processing import process_application, generate_cover_letter
from app.services.file_storage import file_storage

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


@router.get("/{application_id}/download-tailored-resume")
async def download_tailored_resume(
    application_id: int, 
    format: str = Query("docx", description="Format: docx or pdf"),
    db: Session = Depends(get_db)
):
    """Download the tailored resume for a job application."""
    application = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if application is None:
        raise HTTPException(status_code=404, detail="Job application not found")
    
    if not application.tailored_resume_path:
        raise HTTPException(status_code=404, detail="Tailored resume not yet generated")
    
    try:
        # Download from storage
        local_file_path = file_storage.download_file(application.tailored_resume_path)
        
        # Determine filename and media type
        if format.lower() == "pdf":
            filename = f"tailored_resume_{application_id}.pdf"
            media_type = "application/pdf"
        else:
            filename = f"tailored_resume_{application_id}.docx"
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        
        return FileResponse(
            path=local_file_path,
            filename=filename,
            media_type=media_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading tailored resume: {str(e)}")


@router.get("/{application_id}/download-cover-letter")
async def download_cover_letter(
    application_id: int, 
    format: str = Query("docx", description="Format: docx or pdf"),
    db: Session = Depends(get_db)
):
    """Download the cover letter for a job application."""
    application = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if application is None:
        raise HTTPException(status_code=404, detail="Job application not found")
    
    if not application.cover_letter_path:
        raise HTTPException(status_code=404, detail="Cover letter not yet generated")
    
    try:
        # Download from storage
        local_file_path = file_storage.download_file(application.cover_letter_path)
        
        # Determine filename and media type
        if format.lower() == "pdf":
            filename = f"cover_letter_{application_id}.pdf"
            media_type = "application/pdf"
        else:
            filename = f"cover_letter_{application_id}.docx"
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        
        return FileResponse(
            path=local_file_path,
            filename=filename,
            media_type=media_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading cover letter: {str(e)}")


@router.get("/{application_id}/preview")
async def get_application_preview(application_id: int, db: Session = Depends(get_db)):
    """Get a preview of the job application (resume + job info)."""
    application = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if application is None:
        raise HTTPException(status_code=404, detail="Job application not found")
    
    # Get job and resume details
    job = db.query(Job).filter(Job.id == application.job_id).first()
    resume = db.query(Resume).filter(Resume.id == application.resume_id).first()
    
    if not job or not resume:
        raise HTTPException(status_code=404, detail="Job or resume not found")
    
    # Generate resume preview tailored for this job
    from app.services.resume_processing import generate_resume_preview
    preview_task = generate_resume_preview.delay(resume.id, job.id)
    
    return {
        "application_id": application_id,
        "job": {
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location
        },
        "resume": {
            "id": resume.id,
            "filename": resume.filename,
            "status": resume.status
        },
        "application_status": application.status,
        "preview_task_id": preview_task.id,
        "message": "Application preview generation started"
    }


@router.get("/{application_id}/status")
async def get_application_status(application_id: int, db: Session = Depends(get_db)):
    """Get application processing status."""
    application = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if application is None:
        raise HTTPException(status_code=404, detail="Job application not found")
    
    return application
