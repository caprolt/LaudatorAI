"""Pydantic schemas for API requests and responses."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, HttpUrl


# Base schemas
class TimestampSchema(BaseModel):
    """Base schema with timestamps."""
    
    created_at: datetime
    updated_at: datetime


# Job schemas
class JobBase(BaseModel):
    """Base job schema."""
    
    url: HttpUrl
    title: str
    company: str
    location: Optional[str] = None
    description: str
    requirements: Optional[str] = None


class JobCreate(JobBase):
    """Schema for creating a job."""
    pass


class JobUpdate(BaseModel):
    """Schema for updating a job."""
    
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    status: Optional[str] = None
    raw_content: Optional[str] = None
    normalized_content: Optional[str] = None


class JobResponse(JobBase, TimestampSchema):
    """Schema for job response."""
    
    id: int
    status: str
    raw_content: Optional[str] = None
    normalized_content: Optional[str] = None
    
    # Frontend-compatible fields
    requirements: Optional[List[str]] = None  # Changed from str to List[str]
    
    class Config:
        from_attributes = True


# Resume schemas
class ResumeBase(BaseModel):
    """Base resume schema."""
    
    filename: str
    file_path: str
    content_hash: str


class ResumeCreate(ResumeBase):
    """Schema for creating a resume."""
    pass


class ResumeUpdate(BaseModel):
    """Schema for updating a resume."""
    
    parsed_content: Optional[str] = None
    status: Optional[str] = None


class ResumeResponse(ResumeBase, TimestampSchema):
    """Schema for resume response."""
    
    id: int
    parsed_content: Optional[str] = None
    status: str
    
    # Frontend-compatible fields
    content: Optional[Dict[str, Any]] = None  # Structured JSON content
    
    class Config:
        from_attributes = True


# Resume processing schemas
class ResumePreviewRequest(BaseModel):
    """Schema for resume preview request."""
    
    job_id: Optional[int] = None


class ResumePreviewResponse(BaseModel):
    """Schema for resume preview response."""
    
    resume_id: int
    job_id: Optional[int] = None
    html_preview: str
    parsed_content: Dict[str, Any]


class ResumeProcessingResponse(BaseModel):
    """Schema for resume processing response."""
    
    resume_id: int
    status: str
    parsed_content: Optional[Dict[str, Any]] = None
    message: str


# Job Application schemas
class JobApplicationBase(BaseModel):
    """Base job application schema."""
    
    job_id: int
    resume_id: int


class JobApplicationCreate(JobApplicationBase):
    """Schema for creating a job application."""
    pass


class JobApplicationUpdate(BaseModel):
    """Schema for updating a job application."""
    
    tailored_resume_path: Optional[str] = None
    cover_letter_path: Optional[str] = None
    status: Optional[str] = None
    feedback: Optional[str] = None


class JobApplicationResponse(JobApplicationBase, TimestampSchema):
    """Schema for job application response."""
    
    id: int
    tailored_resume_path: Optional[str] = None
    cover_letter_path: Optional[str] = None
    status: str
    feedback: Optional[str] = None
    
    # Frontend-compatible fields
    tailored_resume_url: Optional[str] = None
    cover_letter_url: Optional[str] = None
    job_description_id: Optional[int] = None  # Alias for job_id
    resume_id: Optional[int] = None
    
    class Config:
        from_attributes = True


# Application preview schemas
class ApplicationPreviewResponse(BaseModel):
    """Schema for application preview response."""
    
    application_id: int
    job: Dict[str, Any]
    resume: Dict[str, Any]
    application_status: str
    preview_task_id: str
    message: str


# Processing Task schemas
class ProcessingTaskBase(BaseModel):
    """Base processing task schema."""
    
    task_id: str
    task_type: str
    related_id: Optional[int] = None


class ProcessingTaskCreate(ProcessingTaskBase):
    """Schema for creating a processing task."""
    pass


class ProcessingTaskUpdate(BaseModel):
    """Schema for updating a processing task."""
    
    status: Optional[str] = None
    result: Optional[str] = None


class ProcessingTaskResponse(ProcessingTaskBase, TimestampSchema):
    """Schema for processing task response."""
    
    id: int
    status: str
    result: Optional[str] = None


# Health check schemas
class HealthResponse(BaseModel):
    """Health check response schema."""
    
    status: str
    service: str
    timestamp: datetime


# Job processing schemas
class JobUrlRequest(BaseModel):
    """Schema for job URL processing request."""
    
    url: HttpUrl


class JobProcessingResponse(BaseModel):
    """Schema for job processing response."""
    
    job_id: int
    status: str
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    normalized_content: Optional[Dict[str, Any]] = None
    message: Optional[str] = None


# Error schemas
class ErrorResponse(BaseModel):
    """Error response schema."""
    
    detail: str
    error_code: Optional[str] = None
