# LaudatorAI Architecture

This document provides a comprehensive overview of the LaudatorAI system architecture, design decisions, and technical implementation details.

## Table of Contents

- [System Overview](#system-overview)
- [Architecture Diagram](#architecture-diagram)
- [Technology Stack](#technology-stack)
- [Component Architecture](#component-architecture)
- [Data Flow](#data-flow)
- [Database Design](#database-design)
- [API Design](#api-design)
- [Security Architecture](#security-architecture)
- [Scalability Considerations](#scalability-considerations)
- [Design Decisions](#design-decisions)

## System Overview

LaudatorAI is a full-stack application that automates the creation of tailored resumes and cover letters for job applications. The system uses AI/LLM technology to analyze job descriptions and customize application materials accordingly.

### Core Capabilities

1. **Job Description Extraction**: Scrapes and normalizes job postings from URLs
2. **Resume Processing**: Parses, stores, and tailors resumes to specific jobs
3. **Cover Letter Generation**: Creates personalized cover letters using LLM
4. **Document Generation**: Produces professional DOCX and PDF outputs
5. **Preview & Editing**: Provides diff view for human-in-the-loop refinement

### Design Philosophy

- **Separation of Concerns**: Clear boundaries between frontend, API, and workers
- **Asynchronous Processing**: Long-running tasks handled via Celery queues
- **API-First Design**: RESTful API with comprehensive OpenAPI documentation
- **Modular Services**: Pluggable components (LLM providers, storage backends)
- **Production-Ready**: Logging, monitoring, error handling, and testing built-in

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Next.js 14 (App Router) + TypeScript + Tailwind CSS    │   │
│  │  - Job Description Input                                 │   │
│  │  - Resume Upload Interface                               │   │
│  │  - Preview & Diff UI                                     │   │
│  │  - Results Download                                      │   │
│  └──────────────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTPS/REST API
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                         API Layer                                │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  FastAPI + Pydantic + SQLAlchemy                         │   │
│  │  - Request Validation                                    │   │
│  │  - Authentication & Authorization (Future)               │   │
│  │  - CRUD Operations                                       │   │
│  │  - Task Orchestration                                    │   │
│  │  - Error Handling & Logging                              │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────┬───────────────────────────────┬───────────────────────┘
          │                               │
          ▼                               ▼
┌──────────────────────┐        ┌────────────────────────┐
│   PostgreSQL DB      │        │   Redis Cache/Queue    │
│  - Jobs              │        │  - Celery Broker       │
│  - Resumes           │        │  - Task Results        │
│  - Applications      │        │  - Session Storage     │
│  - Processing Tasks  │        └────────────────────────┘
└──────────────────────┘                   │
          │                                ▼
          │                    ┌───────────────────────────┐
          │                    │   Celery Workers          │
          │                    │  - Job Processing Queue   │
          │                    │  - Resume Processing      │
          │                    │  - Application Tasks      │
          │                    │  - Cleanup Jobs           │
          │                    └───────────────────────────┘
          │                                │
          │                                ▼
          │                    ┌───────────────────────────┐
          └────────────────────┤   Service Layer           │
                               │  - Web Scraping           │
                               │    (Playwright)           │
                               │  - LLM Integration        │
                               │    (OpenAI/Ollama/HF)     │
                               │  - Document Processing    │
                               │    (python-docx/weasyprint│
                               │  - File Storage (MinIO)   │
                               └───────────────────────────┘
                                           │
                                           ▼
                               ┌───────────────────────────┐
                               │   External Services       │
                               │  - LLM APIs               │
                               │  - Job Posting Sites      │
                               │  - S3/MinIO Storage       │
                               └───────────────────────────┘
```

## Technology Stack

### Frontend

| Technology | Purpose | Why Chosen |
|------------|---------|------------|
| **Next.js 14** | React Framework | Server-side rendering, App Router, excellent DX |
| **TypeScript** | Type Safety | Catch errors early, better IDE support |
| **Tailwind CSS** | Styling | Rapid UI development, consistent design |
| **shadcn/ui** | Component Library | Accessible, customizable, well-documented |
| **Radix UI** | Headless Components | Accessibility-first, unstyled primitives |
| **Lucide Icons** | Icons | Consistent, modern icon set |

### Backend

| Technology | Purpose | Why Chosen |
|------------|---------|------------|
| **FastAPI** | API Framework | High performance, automatic docs, async support |
| **Python 3.11+** | Programming Language | Rich ecosystem, excellent for data processing |
| **Pydantic** | Data Validation | Type validation, JSON schema generation |
| **SQLAlchemy** | ORM | Mature, powerful, supports async |
| **Alembic** | Database Migrations | Version control for database schema |
| **Celery** | Task Queue | Distributed task processing, mature |
| **Redis** | Cache/Message Broker | Fast, reliable, perfect for Celery |
| **PostgreSQL** | Database | Robust, feature-rich, ACID compliant |

### Document Processing

| Technology | Purpose | Why Chosen |
|------------|---------|------------|
| **python-docx** | DOCX Generation | Native Python library, well-maintained |
| **WeasyPrint** | PDF Generation | HTML to PDF, excellent rendering |
| **Playwright** | Web Scraping | Modern, reliable, handles dynamic content |
| **readability-lxml** | Content Extraction | Extracts main content from web pages |

### Infrastructure

| Technology | Purpose | Why Chosen |
|------------|---------|------------|
| **Docker** | Containerization | Consistent environments, easy deployment |
| **MinIO** | Object Storage | S3-compatible, self-hosted option |
| **Railway** | Backend Hosting | Easy deployment, managed PostgreSQL/Redis |
| **Vercel** | Frontend Hosting | Optimized for Next.js, global CDN |

## Component Architecture

### Frontend Components

```
frontend/src/
├── app/                          # Next.js App Router
│   ├── page.tsx                 # Home page (main workflow)
│   ├── layout.tsx               # Root layout with providers
│   └── globals.css              # Global styles
│
├── components/                   # React components
│   ├── job-description-input.tsx    # URL input & extraction
│   ├── resume-upload.tsx            # File upload component
│   ├── preview-diff.tsx             # Side-by-side diff view
│   ├── results-page.tsx             # Download results
│   ├── error-boundary.tsx           # Error handling wrapper
│   │
│   └── ui/                          # shadcn/ui components
│       ├── button.tsx
│       ├── card.tsx
│       ├── input.tsx
│       ├── dialog.tsx
│       └── ...
│
├── lib/                          # Utility functions
│   ├── api.ts                   # API client
│   ├── config.ts                # Configuration
│   ├── logger.ts                # Frontend logging
│   └── utils.ts                 # Helper functions
│
└── types/                        # TypeScript types
    └── index.ts                 # Shared type definitions
```

### Backend Components

```
backend/app/
├── api/                          # API layer
│   └── v1/
│       ├── api.py               # Router aggregation
│       ├── logs.py              # Logging middleware
│       └── endpoints/           # API endpoints
│           ├── jobs.py          # Job CRUD
│           ├── resumes.py       # Resume management
│           ├── applications.py  # Application processing
│           └── health.py        # Health checks
│
├── core/                         # Core infrastructure
│   ├── config.py                # Settings (env vars)
│   ├── database.py              # DB connection & sessions
│   ├── celery_app.py            # Celery configuration
│   └── logging.py               # Structured logging
│
├── models/                       # Database models
│   ├── __init__.py              # Model exports
│   ├── job.py                   # Job model
│   ├── resume.py                # Resume model
│   ├── application.py           # Application model
│   └── task.py                  # Processing task model
│
├── schemas/                      # Pydantic schemas
│   ├── __init__.py              # Schema exports
│   ├── job.py                   # Job schemas
│   ├── resume.py                # Resume schemas
│   ├── application.py           # Application schemas
│   └── common.py                # Shared schemas
│
├── services/                     # Business logic
│   ├── job_processing.py        # Job scraping & normalization
│   ├── resume_processing.py     # Resume parsing & tailoring
│   ├── cover_letter_processing.py # Cover letter generation
│   ├── application_processing.py # Full application workflow
│   ├── file_storage.py          # MinIO/S3 operations
│   ├── web_scraping.py          # Playwright scraping
│   ├── jd_normalization.py      # JD extraction
│   └── cleanup.py               # Maintenance tasks
│
├── templates/                    # Document templates
│   ├── default_resume_template.py
│   └── default_cover_letter_template.py
│
├── utils/                        # Utilities
│   └── __init__.py
│
└── main.py                       # Application entry point
```

## Data Flow

### 1. Job Application Workflow

```
User Input (Job URL + Resume File)
    │
    ▼
[Frontend] Validates input
    │
    ▼
[API] POST /api/v1/applications/
    │
    ├─► Validates job URL format
    ├─► Uploads resume to MinIO
    ├─► Creates database records
    └─► Enqueues Celery tasks
            │
            ├─► [Worker] Job Processing
            │       ├─► Scrapes job posting (Playwright)
            │       ├─► Extracts description (Readability)
            │       ├─► Normalizes content (LLM)
            │       └─► Updates database
            │
            ├─► [Worker] Resume Processing
            │       ├─► Parses resume (python-docx)
            │       ├─► Extracts structured data
            │       └─► Stores in database
            │
            └─► [Worker] Application Processing
                    ├─► Tailors resume (LLM)
                    ├─► Generates cover letter (LLM)
                    ├─► Creates DOCX files
                    ├─► Converts to PDF
                    └─► Uploads to MinIO
                            │
                            ▼
                    [Frontend] Polls for status
                            │
                            ▼
                    [Frontend] Downloads results
```

### 2. Resume Tailoring Process

```
Base Resume + Job Description
    │
    ▼
[LLM Prompt Engineering]
    ├─► System prompt defines role
    ├─► User prompt includes:
    │   ├─► Job description
    │   ├─► Base resume JSON
    │   └─► Tailoring instructions
    │
    ▼
[LLM Processing]
    ├─► Analyzes job requirements
    ├─► Identifies relevant skills
    ├─► Reorders/emphasizes content
    └─► Maintains factual accuracy
        │
        ▼
[JSON Output]
    ├─► Structured resume data
    └─► Ready for template rendering
        │
        ▼
[Document Generation]
    ├─► Applies template (python-docx)
    ├─► Formats content
    └─► Exports DOCX & PDF
```

### 3. Cover Letter Generation

```
Job Description + Resume + User Details
    │
    ▼
[Template Selection]
    │
    ▼
[LLM Generation]
    ├─► Analyzes company & role
    ├─► Matches candidate skills
    ├─► Generates personalized content
    └─► Follows professional structure
        │
        ▼
[Document Creation]
    ├─► Applies formatting
    ├─► Inserts user details
    └─► Exports DOCX & PDF
```

## Database Design

### Entity Relationship Diagram

```
┌─────────────────┐         ┌──────────────────┐
│      Jobs       │         │     Resumes      │
├─────────────────┤         ├──────────────────┤
│ id (PK)         │         │ id (PK)          │
│ url             │         │ filename         │
│ title           │    ┌────┤ file_path        │
│ company         │    │    │ content_hash     │
│ description     │    │    │ parsed_content   │
│ requirements    │    │    │ status           │
│ normalized_jd   │    │    │ created_at       │
│ status          │    │    │ updated_at       │
│ created_at      │    │    └──────────────────┘
│ updated_at      │    │              │
└─────────────────┘    │              │
         │             │              │
         │             │              │
         └─────────────┼──────────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │  Job_Applications    │
            ├──────────────────────┤
            │ id (PK)              │
            │ job_id (FK)          │
            │ resume_id (FK)       │
            │ tailored_resume_path │
            │ cover_letter_path    │
            │ status               │
            │ created_at           │
            │ updated_at           │
            └──────────────────────┘
                       │
                       │
                       ▼
            ┌──────────────────────┐
            │  Processing_Tasks    │
            ├──────────────────────┤
            │ id (PK)              │
            │ task_id (Celery)     │
            │ task_type            │
            │ entity_type          │
            │ entity_id            │
            │ status               │
            │ result               │
            │ error_message        │
            │ created_at           │
            │ updated_at           │
            └──────────────────────┘
```

### Table Schemas

#### Jobs Table

```sql
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    url TEXT NOT NULL UNIQUE,
    title VARCHAR(500),
    company VARCHAR(500),
    location VARCHAR(500),
    description TEXT,
    requirements TEXT,
    normalized_jd JSONB,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_created_at ON jobs(created_at);
```

#### Resumes Table

```sql
CREATE TABLE resumes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename VARCHAR(500) NOT NULL,
    file_path TEXT NOT NULL,
    content_hash VARCHAR(64) UNIQUE,
    original_content TEXT,
    parsed_content JSONB,
    status VARCHAR(50) DEFAULT 'uploaded',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_resumes_content_hash ON resumes(content_hash);
CREATE INDEX idx_resumes_status ON resumes(status);
```

#### Job_Applications Table

```sql
CREATE TABLE job_applications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
    resume_id UUID REFERENCES resumes(id) ON DELETE CASCADE,
    tailored_resume_path TEXT,
    tailored_resume_pdf_path TEXT,
    cover_letter_path TEXT,
    cover_letter_pdf_path TEXT,
    status VARCHAR(50) DEFAULT 'processing',
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_applications_job_id ON job_applications(job_id);
CREATE INDEX idx_applications_resume_id ON job_applications(resume_id);
CREATE INDEX idx_applications_status ON job_applications(status);
```

## API Design

### RESTful Principles

- **Resource-based URLs**: `/api/v1/jobs`, `/api/v1/resumes`
- **HTTP Methods**: GET (read), POST (create), PUT (update), DELETE (delete)
- **Status Codes**: Proper HTTP status codes (200, 201, 400, 404, 500)
- **JSON Format**: All requests/responses use JSON
- **Versioning**: API version in URL path (`/api/v1/`)

### Endpoint Structure

```
/api/v1/
├── /jobs/
│   ├── GET    /              # List all jobs (paginated)
│   ├── POST   /              # Create new job
│   ├── GET    /{id}          # Get job by ID
│   ├── PUT    /{id}          # Update job
│   └── DELETE /{id}          # Delete job
│
├── /resumes/
│   ├── GET    /              # List all resumes (paginated)
│   ├── POST   /upload        # Upload new resume
│   ├── GET    /{id}          # Get resume by ID
│   ├── PUT    /{id}          # Update resume metadata
│   └── DELETE /{id}          # Delete resume
│
├── /applications/
│   ├── GET    /              # List applications (paginated)
│   ├── POST   /              # Create application
│   ├── GET    /{id}          # Get application by ID
│   ├── PUT    /{id}          # Update application
│   ├── DELETE /{id}          # Delete application
│   ├── POST   /{id}/generate-cover-letter  # Generate cover letter
│   └── GET    /{id}/download/{file_type}   # Download files
│
└── /health                   # Health check endpoint
```

### Request/Response Examples

See [docs/API_EXAMPLES.md](docs/API_EXAMPLES.md) for detailed API examples.

## Security Architecture

### Current Implementation

1. **Input Validation**: Pydantic schemas validate all inputs
2. **File Upload Security**: 
   - File type validation (DOCX, PDF, DOC only)
   - File size limits (10MB default)
   - Content hash verification
3. **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
4. **CORS Configuration**: Controlled cross-origin access
5. **Error Handling**: Sanitized error messages (no stack traces in production)
6. **Logging**: Request tracking without sensitive data

### Future Enhancements

- [ ] Authentication & Authorization (JWT tokens)
- [ ] Rate limiting (per user/IP)
- [ ] API key management
- [ ] Request encryption (HTTPS enforced)
- [ ] DDoS protection
- [ ] Security headers (HSTS, CSP, etc.)
- [ ] Data encryption at rest
- [ ] Audit logging

## Scalability Considerations

### Horizontal Scaling

- **Stateless API**: FastAPI instances can scale horizontally
- **Worker Scaling**: Add more Celery workers as needed
- **Database**: PostgreSQL supports read replicas
- **File Storage**: S3/MinIO handles large file volumes
- **Caching**: Redis can be clustered

### Performance Optimizations

1. **Database Indexing**: Strategic indexes on frequently queried columns
2. **Connection Pooling**: SQLAlchemy connection pool
3. **Async Operations**: FastAPI async endpoints for I/O operations
4. **Background Tasks**: Offload heavy processing to Celery
5. **CDN**: Static assets served via Vercel CDN
6. **Lazy Loading**: Frontend loads components on demand

### Bottleneck Mitigation

| Potential Bottleneck | Solution |
|---------------------|----------|
| LLM API rate limits | Queue management, retries, fallback providers |
| Web scraping blocks | Rotating proxies, rate limiting, retry logic |
| Database queries | Indexes, query optimization, read replicas |
| File uploads | Chunked uploads, compression, direct S3 upload |
| Worker capacity | Auto-scaling Celery workers, task prioritization |

## Design Decisions

### 1. Why FastAPI over Django/Flask?

**Decision**: Use FastAPI for the backend API

**Rationale**:
- ✅ Automatic OpenAPI documentation
- ✅ Native async/await support
- ✅ Excellent performance (comparable to Node.js)
- ✅ Type hints with Pydantic validation
- ✅ Modern Python 3.11+ features

### 2. Why Next.js over Create React App?

**Decision**: Use Next.js 14 with App Router

**Rationale**:
- ✅ Server-side rendering for better SEO
- ✅ File-based routing
- ✅ Built-in optimization (images, fonts, etc.)
- ✅ Excellent developer experience
- ✅ Vercel deployment integration

### 3. Why Celery over Direct API Processing?

**Decision**: Use Celery for background task processing

**Rationale**:
- ✅ Non-blocking API responses
- ✅ Retry logic for failed tasks
- ✅ Task prioritization and routing
- ✅ Distributed processing capability
- ✅ Monitoring and observability

### 4. Why PostgreSQL over MongoDB?

**Decision**: Use PostgreSQL for primary database

**Rationale**:
- ✅ ACID compliance for data integrity
- ✅ Strong typing and constraints
- ✅ JSON/JSONB support for flexible data
- ✅ Mature ecosystem and tooling
- ✅ Better for relational data (jobs, resumes, applications)

### 5. Why MinIO/S3 over Database Blob Storage?

**Decision**: Use object storage for files

**Rationale**:
- ✅ Scalable storage independent of database
- ✅ Presigned URLs for secure access
- ✅ Cost-effective for large files
- ✅ S3-compatible for easy cloud migration
- ✅ Better separation of concerns

### 6. Why python-docx over Python-DOCX or Similar?

**Decision**: Use python-docx for DOCX generation

**Rationale**:
- ✅ Native Python library (no external dependencies)
- ✅ Well-maintained and documented
- ✅ Full control over document structure
- ✅ Supports complex formatting
- ✅ Easy integration with templates

### 7. Why Playwright over Selenium/Scrapy?

**Decision**: Use Playwright for web scraping

**Rationale**:
- ✅ Modern API with excellent documentation
- ✅ Handles dynamic JavaScript content
- ✅ Built-in waiting and retry logic
- ✅ Better performance than Selenium
- ✅ Supports multiple browsers

## Monitoring & Observability

### Logging Strategy

- **Structured Logging**: JSON format for easy parsing
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Request Tracking**: Unique request IDs
- **Contextual Information**: User ID, task ID, operation type

### Metrics (Future)

- API response times
- Task processing duration
- Error rates
- Queue depths
- Resource utilization

### Alerting (Future)

- Failed task threshold
- API error rate spike
- Database connection issues
- Storage capacity warnings

## Future Architecture Enhancements

### Phase 2 Features

- [ ] Multi-tenancy support
- [ ] Real-time status updates (WebSockets)
- [ ] Advanced caching strategies
- [ ] GraphQL API option
- [ ] Microservices architecture
- [ ] Event-driven architecture

### Advanced Features

- [ ] Vector embeddings for semantic search (Qdrant/FAISS)
- [ ] ATS optimization scoring
- [ ] Company research integration
- [ ] Multi-language support
- [ ] Custom template builder
- [ ] Interview preparation tools

---

**Document Version**: 1.0  
**Last Updated**: 2024-12-19  
**Maintainers**: LaudatorAI Team
