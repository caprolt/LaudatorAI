"""Main FastAPI application entry point."""

import time
import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import init_db
from app.core.logging import setup_logging, log_request
from app.api.v1.api import api_router

# Initialize logging
logger = setup_logging()

app = FastAPI(
    title="LaudatorAI API",
    description="AI-Powered Job Application Assistant",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set up CORS with fallback for empty origins
cors_origins = settings.CORS_ORIGINS
if not cors_origins:
    # Fallback to allow all origins in development
    cors_origins = ["*"]
    logger.warning("No CORS origins configured, allowing all origins")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add request processing time and logging."""
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    # Add request ID to request state
    request.state.request_id = request_id
    
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Request-ID"] = request_id
    
    # Log request
    log_request(
        request_id=request_id,
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration=process_time
    )
    
    return response


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("Starting LaudatorAI API")
    logger.info(f"CORS origins: {cors_origins}")
    
    # Initialize database (optional for now)
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        logger.warning("Application starting without database connection")
        # Don't fail startup - let the app run without DB for now


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("Shutting down LaudatorAI API")


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to LaudatorAI API"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Simple health check - just return success
        # We'll add database check later once basic connectivity works
        return {
            "status": "healthy", 
            "service": "LaudatorAI API", 
            "timestamp": time.time(),
            "version": "0.1.0",
            "environment": settings.ENVIRONMENT
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy", 
            "service": "LaudatorAI API", 
            "timestamp": time.time(),
            "version": "0.1.0",
            "environment": settings.ENVIRONMENT,
            "error": str(e)
        }


@app.get("/api/v1/health")
async def api_health_check():
    """API health check endpoint."""
    return await health_check()


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error(f"Unhandled exception: {exc} | request_id={request_id}")
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "request_id": request_id
        }
    )
