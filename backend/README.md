# LaudatorAI Backend

AI-Powered Job Application Assistant Backend API.

## Features

- FastAPI-based REST API with comprehensive CRUD operations
- Job description extraction and processing
- Resume parsing, storage, and tailoring
- Cover letter generation
- File storage with MinIO/S3
- Background task processing with Celery and Redis
- Database management with SQLAlchemy and Alembic
- Comprehensive logging and observability
- Health monitoring and error handling

## Architecture Overview

### Core Components

1. **Database Models** (`app/models/`)
   - Job: Job posting information and processing status
   - Resume: Resume file metadata and parsed content
   - JobApplication: Links jobs and resumes for applications
   - ProcessingTask: Tracks Celery task status and results

2. **API Endpoints** (`app/api/v1/endpoints/`)
   - `/jobs/`: Complete CRUD operations for job postings
   - `/resumes/`: Resume upload, storage, and management
   - `/applications/`: Job application processing and management
   - `/health/`: Health check and monitoring

3. **Background Services** (`app/services/`)
   - Job processing with web scraping capabilities
   - Resume parsing and content extraction
   - Application processing and document generation
   - File storage management (MinIO/S3)
   - System cleanup and maintenance tasks

4. **Infrastructure** (`app/core/`)
   - Database connection and session management
   - Celery task queue configuration
   - File storage service integration
   - Logging and observability setup
   - Configuration management

## Technology Stack

- **Framework**: FastAPI with automatic API documentation
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Migrations**: Alembic for database schema management
- **Task Queue**: Celery with Redis broker
- **File Storage**: MinIO/S3 compatible storage
- **Document Processing**: python-docx, weasyprint
- **Web Scraping**: Playwright, readability-lxml
- **LLM Integration**: OpenAI, Ollama, Hugging Face
- **Monitoring**: Structured logging with request tracking

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL
- Redis
- MinIO (or S3-compatible storage)

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy environment file:
```bash
cp .env.example .env
```

4. Update `.env` with your configuration.

5. Initialize the database:
```bash
python scripts/init_db.py
```

### Running the Application

1. Start the main API server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

2. Start Celery worker (in separate terminal):
```bash
python scripts/start_celery_worker.py
```

3. Start Celery beat scheduler (optional, for periodic tasks):
```bash
celery -A app.core.celery_app beat --loglevel=info
```

### Docker Setup

The entire stack can be run with Docker Compose:

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database
- Redis for Celery broker
- MinIO for file storage
- FastAPI backend
- Next.js frontend

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Jobs
- `POST /api/v1/jobs/` - Create a new job posting
- `GET /api/v1/jobs/` - List all jobs with pagination
- `GET /api/v1/jobs/{job_id}` - Get job by ID
- `PUT /api/v1/jobs/{job_id}` - Update job details
- `DELETE /api/v1/jobs/{job_id}` - Delete job

### Resumes
- `POST /api/v1/resumes/upload` - Upload a resume file (PDF, DOCX, DOC)
- `GET /api/v1/resumes/` - List all resumes with pagination
- `GET /api/v1/resumes/{resume_id}` - Get resume by ID
- `PUT /api/v1/resumes/{resume_id}` - Update resume metadata
- `DELETE /api/v1/resumes/{resume_id}` - Delete resume and associated files

### Applications
- `POST /api/v1/applications/` - Create a job application (links job and resume)
- `GET /api/v1/applications/` - List all applications with pagination
- `GET /api/v1/applications/{application_id}` - Get application by ID
- `PUT /api/v1/applications/{application_id}` - Update application details
- `DELETE /api/v1/applications/{application_id}` - Delete application
- `POST /api/v1/applications/{application_id}/generate-cover-letter` - Generate cover letter

### Health & Monitoring
- `GET /health` - Health check endpoint
- `GET /` - Root endpoint with API information

## Background Tasks

The system uses Celery for background task processing with dedicated queues:

- **job_processing**: Web scraping and job description extraction
- **resume_processing**: Resume parsing and content structuring
- **application_processing**: Document generation and tailoring
- **cleanup**: System maintenance and cleanup tasks

### Task Types
- Job posting processing and normalization
- Resume parsing and content extraction
- Resume tailoring for specific jobs
- Cover letter generation
- File cleanup and maintenance

## File Storage

Files are stored in MinIO/S3 with organized structure:
- `resumes/{hash}_{filename}` - Uploaded resume files
- `tailored/{application_id}_resume.{ext}` - Tailored resumes
- `cover_letters/{application_id}_cover_letter.{ext}` - Generated cover letters

Features:
- Automatic file deduplication using SHA256 hashing
- Presigned URLs for secure file access
- File type validation and security
- Automatic cleanup of temporary files

## Database Schema

### Core Tables
- **jobs**: Job postings with processing status
- **resumes**: Resume files with metadata and parsed content
- **job_applications**: Links between jobs and resumes
- **processing_tasks**: Celery task tracking and results

### Features
- Automatic timestamps (created_at, updated_at)
- Status tracking for all entities
- Content hashing for deduplication
- Foreign key relationships with proper indexing

## Development

### Code Formatting

```bash
# Format code
black app/

# Sort imports
isort app/

# Type checking
mypy app/

# Linting
flake8 app/
```

### Running Tests

```bash
pytest
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Check migration status
alembic current
```

### Monitoring and Logging

The application includes comprehensive logging:
- Request/response logging with timing
- Task execution tracking
- File operation monitoring
- Error tracking and reporting
- Structured logging for easy parsing

## Project Structure

```
app/
├── api/                    # API endpoints
│   └── v1/
│       ├── api.py         # Main API router
│       └── endpoints/     # Individual endpoint modules
│           ├── health.py  # Health check endpoints
│           ├── jobs.py    # Job management endpoints
│           ├── resumes.py # Resume management endpoints
│           └── applications.py # Application endpoints
├── core/                  # Core application modules
│   ├── config.py         # Configuration settings
│   ├── database.py       # Database connection and session
│   ├── celery_app.py     # Celery configuration
│   └── logging.py        # Logging setup
├── models/               # SQLAlchemy database models
├── schemas/              # Pydantic request/response schemas
├── services/             # Business logic and background tasks
│   ├── file_storage.py   # MinIO/S3 file operations
│   ├── job_processing.py # Job processing tasks
│   ├── resume_processing.py # Resume processing tasks
│   ├── application_processing.py # Application tasks
│   └── cleanup.py        # System cleanup tasks
├── utils/                # Utility functions
└── main.py              # Application entry point

scripts/
├── init_db.py           # Database initialization
└── start_celery_worker.py # Celery worker startup

alembic/                 # Database migrations
├── env.py              # Migration environment
├── script.py.mako      # Migration template
└── versions/           # Migration files
```

## Phase 2 Implementation Status

✅ **Completed Components:**
- FastAPI application structure with middleware and error handling
- PostgreSQL database with SQLAlchemy ORM and Alembic migrations
- Redis configuration for Celery broker with task routing
- Complete CRUD API endpoints for jobs, resumes, and applications
- MinIO/S3 file storage service with upload/download capabilities
- Comprehensive logging and observability setup
- Background task processing with Celery workers
- Database models and Pydantic schemas for all entities
- Health check and monitoring endpoints
- File deduplication and validation
- Request tracking and performance monitoring

🔄 **Next Steps (Phase 3):**
- Implement job posting URL ingestion and web scraping
- Add job description normalization and extraction logic
- Build JD processing API endpoints with validation
- Add error handling and retry mechanisms for job processing
- Implement content parsing and structuring algorithms
