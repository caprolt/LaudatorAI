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

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
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
    
    # Initialize database
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        # Don't raise the exception - let the app start even if DB fails
        # This allows the health check to work even if DB is not available
        logger.warning("Application starting without database connection")


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
        # Test database connection
        from app.core.database import engine
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        
        return {
            "status": "healthy", 
            "service": "LaudatorAI API", 
            "timestamp": time.time(),
            "version": "0.1.0",
            "database": "connected"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        # Return 200 even if DB fails, but indicate the issue
        return {
            "status": "degraded", 
            "service": "LaudatorAI API", 
            "timestamp": time.time(),
            "version": "0.1.0",
            "database": "disconnected",
            "error": str(e)
        }


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
