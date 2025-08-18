"""Resume processing endpoints."""

import os
import tempfile
from typing import List
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import ResumeCreate, ResumeResponse, ResumeUpdate
from app.models import Resume
from app.services.file_storage import file_storage, calculate_file_hash, is_valid_file_type
from app.services.resume_processing import parse_resume, generate_resume_preview
from app.templates.default_resume_template import list_templates

router = APIRouter()

# Allowed file types for resumes
ALLOWED_RESUME_EXTENSIONS = [".pdf", ".docx", ".doc"]


@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a resume file."""
    try:
        # Validate file type
        if not is_valid_file_type(file.filename, ALLOWED_RESUME_EXTENSIONS):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_RESUME_EXTENSIONS)}"
            )
        
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Calculate file hash
            file_hash = calculate_file_hash(temp_file_path)
            
            # Check if file already exists
            existing_resume = db.query(Resume).filter(Resume.content_hash == file_hash).first()
            if existing_resume:
                os.unlink(temp_file_path)
                return existing_resume
            
            # Upload to file storage
            object_name = f"resumes/{file_hash}_{file.filename}"
            file_path = file_storage.upload_file(temp_file_path, object_name)
            
            # Create resume record
            db_resume = Resume(
                filename=file.filename,
                file_path=file_path,
                content_hash=file_hash
            )
            
            db.add(db_resume)
            db.commit()
            db.refresh(db_resume)
            
            # Start background parsing
            parse_resume.delay(db_resume.id, file_path)
            
            return db_resume
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except Exception as e:
        # Log the error and return a proper error response
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in upload_resume: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/", response_model=List[ResumeResponse])
async def list_resumes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all resumes."""
    resumes = db.query(Resume).offset(skip).limit(limit).all()
    return resumes


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(resume_id: int, db: Session = Depends(get_db)):
    """Get resume by ID."""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


@router.put("/{resume_id}", response_model=ResumeResponse)
async def update_resume(resume_id: int, resume_update: ResumeUpdate, db: Session = Depends(get_db)):
    """Update resume by ID."""
    db_resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Update fields
    update_data = resume_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_resume, field, value)
    
    db.commit()
    db.refresh(db_resume)
    return db_resume


@router.delete("/{resume_id}")
async def delete_resume(resume_id: int, db: Session = Depends(get_db)):
    """Delete resume by ID."""
    db_resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Delete from file storage
    try:
        file_storage.delete_file(db_resume.file_path)
    except Exception as e:
        # Log error but don't fail the request
        pass
    
    db.delete(db_resume)
    db.commit()
    return {"message": "Resume deleted successfully"}


@router.post("/{resume_id}/preview")
async def generate_preview(
    resume_id: int, 
    job_id: int = Query(None, description="Optional job ID to tailor the preview"),
    db: Session = Depends(get_db)
):
    """Generate a preview of the resume."""
    # Verify resume exists
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Verify job exists if provided
    if job_id:
        from app.models import Job
        job = db.query(Job).filter(Job.id == job_id).first()
        if job is None:
            raise HTTPException(status_code=404, detail="Job not found")
    
    # Start background preview generation
    preview_task = generate_resume_preview.delay(resume_id, job_id)
    
    return {
        "message": "Resume preview generation started",
        "resume_id": resume_id,
        "job_id": job_id,
        "task_id": preview_task.id
    }


@router.get("/{resume_id}/preview")
async def get_preview(resume_id: int, db: Session = Depends(get_db)):
    """Get the latest preview of the resume."""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    if not resume.parsed_content:
        raise HTTPException(status_code=400, detail="Resume not yet parsed")
    
    import json
    parsed_content = json.loads(resume.parsed_content)
    
    # Generate simple HTML preview
    from app.services.resume_processing import _generate_html_preview
    html_preview = _generate_html_preview(parsed_content)
    
    return {
        "resume_id": resume_id,
        "html_preview": html_preview,
        "parsed_content": parsed_content
    }


@router.get("/{resume_id}/download")
async def download_resume(resume_id: int, db: Session = Depends(get_db)):
    """Download the original resume file."""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    try:
        # Download from storage
        local_file_path = file_storage.download_file(resume.file_path)
        
        return FileResponse(
            path=local_file_path,
            filename=resume.filename,
            media_type='application/octet-stream'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading file: {str(e)}")


@router.get("/templates/list")
async def list_resume_templates():
    """List available resume templates."""
    templates = list_templates()
    return {
        "templates": templates,
        "count": len(templates)
    }
