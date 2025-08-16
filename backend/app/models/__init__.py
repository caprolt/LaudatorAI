"""Database models for LaudatorAI."""

from sqlalchemy import Column, DateTime, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps."""
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Job(Base, TimestampMixin):
    """Job posting model."""
    
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    company = Column(String(200), nullable=False)
    location = Column(String(200))
    description = Column(Text, nullable=False)
    requirements = Column(Text)
    status = Column(String(50), default="pending")  # pending, processing, completed, failed
    raw_content = Column(Text)  # Raw scraped content
    normalized_content = Column(Text)  # Processed/normalized content


class Resume(Base, TimestampMixin):
    """Resume model."""
    
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)  # Path in MinIO/S3
    content_hash = Column(String(64), nullable=False, index=True)  # SHA256 hash
    parsed_content = Column(Text)  # Structured JSON content
    status = Column(String(50), default="pending")  # pending, parsed, tailored, failed


class JobApplication(Base, TimestampMixin):
    """Job application model linking jobs and resumes."""
    
    __tablename__ = "job_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, nullable=False, index=True)
    resume_id = Column(Integer, nullable=False, index=True)
    tailored_resume_path = Column(String(500))  # Path to tailored resume
    cover_letter_path = Column(String(500))  # Path to cover letter
    status = Column(String(50), default="pending")  # pending, processing, completed, failed
    feedback = Column(Text)  # User feedback or notes


class ProcessingTask(Base, TimestampMixin):
    """Celery task tracking model."""
    
    __tablename__ = "processing_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(255), nullable=False, unique=True, index=True)  # Celery task ID
    task_type = Column(String(100), nullable=False)  # job_processing, resume_parsing, etc.
    status = Column(String(50), default="pending")  # pending, running, completed, failed
    result = Column(Text)  # Task result or error message
    related_id = Column(Integer)  # ID of related record (job_id, resume_id, etc.)
