"""Job description processing endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class JobURLRequest(BaseModel):
    """Request model for job URL processing."""
    url: str


class JobDescriptionResponse(BaseModel):
    """Response model for job description."""
    id: str
    url: str
    title: str
    company: str
    description: str
    requirements: list[str]
    status: str


@router.post("/extract", response_model=JobDescriptionResponse)
async def extract_job_description(request: JobURLRequest):
    """Extract job description from URL."""
    # TODO: Implement job description extraction
    # This will be implemented in Phase 3
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/{job_id}", response_model=JobDescriptionResponse)
async def get_job_description(job_id: str):
    """Get job description by ID."""
    # TODO: Implement job description retrieval
    # This will be implemented in Phase 3
    raise HTTPException(status_code=501, detail="Not implemented yet")
