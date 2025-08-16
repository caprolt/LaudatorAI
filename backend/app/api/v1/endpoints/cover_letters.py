"""Cover letter API endpoints."""

from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel

from app.services.cover_letter_processing import generate_cover_letter, preview_cover_letter
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


class CoverLetterPreviewRequest(BaseModel):
    """Request model for cover letter preview."""
    job_description: Dict[str, Any]
    resume_data: Dict[str, Any]
    personal_info: Dict[str, Any]


class CoverLetterGenerateRequest(BaseModel):
    """Request model for cover letter generation."""
    application_id: int
    job_id: int
    resume_id: int


class CoverLetterResponse(BaseModel):
    """Response model for cover letter operations."""
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None
    task_id: Optional[str] = None


@router.post("/preview", response_model=CoverLetterResponse)
async def preview_cover_letter_endpoint(
    request: CoverLetterPreviewRequest,
    background_tasks: BackgroundTasks
) -> CoverLetterResponse:
    """Generate a preview cover letter without saving to storage."""
    try:
        logger.info("Starting cover letter preview generation")
        
        # Start the preview task
        task = preview_cover_letter.delay(
            request.job_description,
            request.resume_data,
            request.personal_info
        )
        
        return CoverLetterResponse(
            status="processing",
            message="Cover letter preview generation started",
            task_id=task.id
        )
        
    except Exception as e:
        logger.error(f"Error starting cover letter preview: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to start cover letter preview: {str(e)}")


@router.post("/generate", response_model=CoverLetterResponse)
async def generate_cover_letter_endpoint(
    request: CoverLetterGenerateRequest,
    background_tasks: BackgroundTasks
) -> CoverLetterResponse:
    """Generate a cover letter for a job application."""
    try:
        logger.info(f"Starting cover letter generation for application {request.application_id}")
        
        # Start the generation task
        task = generate_cover_letter.delay(
            request.application_id,
            request.job_id,
            request.resume_id
        )
        
        return CoverLetterResponse(
            status="processing",
            message="Cover letter generation started",
            task_id=task.id
        )
        
    except Exception as e:
        logger.error(f"Error starting cover letter generation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to start cover letter generation: {str(e)}")


@router.get("/status/{task_id}", response_model=CoverLetterResponse)
async def get_cover_letter_status(task_id: str) -> CoverLetterResponse:
    """Get the status of a cover letter generation task."""
    try:
        from app.core.celery_app import celery_app
        
        # Get task result
        task_result = celery_app.AsyncResult(task_id)
        
        if task_result.ready():
            if task_result.successful():
                result = task_result.result
                return CoverLetterResponse(
                    status="completed",
                    message="Cover letter generation completed successfully",
                    data=result
                )
            else:
                return CoverLetterResponse(
                    status="failed",
                    message=f"Cover letter generation failed: {task_result.info}"
                )
        else:
            return CoverLetterResponse(
                status="processing",
                message="Cover letter generation in progress"
            )
            
    except Exception as e:
        logger.error(f"Error getting cover letter status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get cover letter status: {str(e)}")


@router.get("/templates", response_model=Dict[str, Any])
async def get_cover_letter_templates() -> Dict[str, Any]:
    """Get available cover letter templates."""
    try:
        from app.templates.default_cover_letter_template import get_template, get_template_variants
        
        templates = {
            "default": get_template(),
            "variants": get_template_variants()
        }
        
        return {
            "status": "success",
            "message": "Cover letter templates retrieved successfully",
            "data": templates
        }
        
    except Exception as e:
        logger.error(f"Error getting cover letter templates: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get cover letter templates: {str(e)}")


@router.post("/validate", response_model=Dict[str, Any])
async def validate_cover_letter_data(request: CoverLetterPreviewRequest) -> Dict[str, Any]:
    """Validate cover letter data structure."""
    try:
        from app.templates.default_cover_letter_template import validate_template_data, format_template_data
        
        # Validate the data
        is_valid = validate_template_data({
            **request.personal_info,
            "company": request.job_description.get("company", ""),
            "greeting": "Dear Hiring Manager,",
            "opening": "Sample opening",
            "body": "Sample body",
            "closing": "Sample closing",
            "signature": f"Sincerely,\n{request.personal_info.get('name', '')}"
        })
        
        if is_valid:
            return {
                "status": "success",
                "message": "Cover letter data is valid",
                "valid": True
            }
        else:
            return {
                "status": "error",
                "message": "Cover letter data is invalid - missing required fields",
                "valid": False
            }
            
    except Exception as e:
        logger.error(f"Error validating cover letter data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to validate cover letter data: {str(e)}")


@router.get("/health", response_model=Dict[str, Any])
async def cover_letter_health_check() -> Dict[str, Any]:
    """Health check for cover letter service."""
    try:
        # Check if LLM client can be initialized
        from app.services.cover_letter_processing import CoverLetterGenerator
        
        # This will test the LLM configuration
        generator = CoverLetterGenerator()
        
        return {
            "status": "healthy",
            "message": "Cover letter service is operational",
            "llm_provider": "openai",  # TODO: Make this dynamic
            "templates_available": True
        }
        
    except Exception as e:
        logger.error(f"Cover letter health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "message": f"Cover letter service is not operational: {str(e)}",
            "llm_provider": "unknown",
            "templates_available": False
        }
