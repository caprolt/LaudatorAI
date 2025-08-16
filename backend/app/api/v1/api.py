"""Main API router for v1 endpoints."""

from fastapi import APIRouter

from app.api.v1.endpoints import health, jobs, resumes

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, tags=["health"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(resumes.router, prefix="/resumes", tags=["resumes"])
