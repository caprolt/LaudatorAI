# API Documentation & Examples

This document provides detailed examples of API requests and responses for the LaudatorAI backend API.

## Table of Contents

- [Base URL](#base-url)
- [Authentication](#authentication)
- [Jobs API](#jobs-api)
- [Resumes API](#resumes-api)
- [Applications API](#applications-api)
- [Health Check](#health-check)
- [Error Responses](#error-responses)
- [Status Codes](#status-codes)

## Base URL

### Development
```
http://localhost:8000
```

### Production
```
https://your-api-domain.com
```

### API Versioning
All API endpoints are prefixed with `/api/v1/`

## Authentication

**Current Status**: No authentication required (MVP)

**Future**: JWT-based authentication will be implemented.

```bash
# Future authentication header
Authorization: Bearer <your_jwt_token>
```

## Jobs API

### Create Job

Create a new job posting from a URL.

**Endpoint**: `POST /api/v1/jobs/`

**Request**:
```bash
curl -X POST "http://localhost:8000/api/v1/jobs/" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/jobs/software-engineer"
  }'
```

**Request Body**:
```json
{
  "url": "https://example.com/jobs/software-engineer"
}
```

**Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "url": "https://example.com/jobs/software-engineer",
  "title": "Senior Software Engineer",
  "company": "Example Corp",
  "location": "San Francisco, CA",
  "description": "We are looking for a Senior Software Engineer...",
  "requirements": "5+ years of experience with Python...",
  "normalized_jd": {
    "role": "Software Engineer",
    "level": "Senior",
    "skills": ["Python", "FastAPI", "PostgreSQL", "AWS"],
    "experience_years": 5,
    "responsibilities": [
      "Design and implement scalable APIs",
      "Lead technical discussions",
      "Mentor junior developers"
    ]
  },
  "status": "completed",
  "created_at": "2024-12-19T10:00:00Z",
  "updated_at": "2024-12-19T10:00:30Z"
}
```

### List Jobs

Get a paginated list of all jobs.

**Endpoint**: `GET /api/v1/jobs/`

**Query Parameters**:
- `skip` (integer, default: 0): Number of records to skip
- `limit` (integer, default: 10, max: 100): Maximum number of records to return

**Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/jobs/?skip=0&limit=10"
```

**Response** (200 OK):
```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "url": "https://example.com/jobs/software-engineer",
      "title": "Senior Software Engineer",
      "company": "Example Corp",
      "location": "San Francisco, CA",
      "status": "completed",
      "created_at": "2024-12-19T10:00:00Z",
      "updated_at": "2024-12-19T10:00:30Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "url": "https://example.com/jobs/frontend-developer",
      "title": "Frontend Developer",
      "company": "Tech Startup",
      "location": "Remote",
      "status": "processing",
      "created_at": "2024-12-19T11:00:00Z",
      "updated_at": "2024-12-19T11:00:00Z"
    }
  ],
  "total": 25,
  "skip": 0,
  "limit": 10
}
```

### Get Job by ID

Retrieve details of a specific job.

**Endpoint**: `GET /api/v1/jobs/{job_id}`

**Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/jobs/550e8400-e29b-41d4-a716-446655440000"
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "url": "https://example.com/jobs/software-engineer",
  "title": "Senior Software Engineer",
  "company": "Example Corp",
  "location": "San Francisco, CA",
  "description": "We are looking for a Senior Software Engineer to join our growing team...",
  "requirements": "- 5+ years of experience with Python\n- Experience with FastAPI or similar frameworks\n- Strong understanding of PostgreSQL\n- AWS experience preferred",
  "normalized_jd": {
    "role": "Software Engineer",
    "level": "Senior",
    "skills": ["Python", "FastAPI", "PostgreSQL", "AWS"],
    "experience_years": 5,
    "responsibilities": [
      "Design and implement scalable APIs",
      "Lead technical discussions",
      "Mentor junior developers"
    ],
    "qualifications": [
      "5+ years Python experience",
      "FastAPI or similar framework experience",
      "PostgreSQL expertise",
      "AWS knowledge"
    ]
  },
  "status": "completed",
  "created_at": "2024-12-19T10:00:00Z",
  "updated_at": "2024-12-19T10:00:30Z"
}
```

### Update Job

Update job details.

**Endpoint**: `PUT /api/v1/jobs/{job_id}`

**Request**:
```bash
curl -X PUT "http://localhost:8000/api/v1/jobs/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Backend Engineer",
    "company": "Example Corp (Updated)"
  }'
```

**Request Body**:
```json
{
  "title": "Senior Backend Engineer",
  "company": "Example Corp (Updated)"
}
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "url": "https://example.com/jobs/software-engineer",
  "title": "Senior Backend Engineer",
  "company": "Example Corp (Updated)",
  "location": "San Francisco, CA",
  "description": "We are looking for a Senior Software Engineer...",
  "status": "completed",
  "created_at": "2024-12-19T10:00:00Z",
  "updated_at": "2024-12-19T12:00:00Z"
}
```

### Delete Job

Delete a job posting.

**Endpoint**: `DELETE /api/v1/jobs/{job_id}`

**Request**:
```bash
curl -X DELETE "http://localhost:8000/api/v1/jobs/550e8400-e29b-41d4-a716-446655440000"
```

**Response** (204 No Content)

## Resumes API

### Upload Resume

Upload a resume file (PDF, DOCX, or DOC).

**Endpoint**: `POST /api/v1/resumes/upload`

**Request**:
```bash
curl -X POST "http://localhost:8000/api/v1/resumes/upload" \
  -F "file=@/path/to/resume.pdf"
```

**Response** (201 Created):
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440000",
  "filename": "resume.pdf",
  "file_path": "resumes/a3b2c1d4e5f6.../resume.pdf",
  "content_hash": "a3b2c1d4e5f67890abcdef1234567890",
  "parsed_content": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-0123",
    "summary": "Experienced software engineer with 5+ years...",
    "experience": [
      {
        "company": "Tech Company",
        "title": "Senior Software Engineer",
        "duration": "2020 - Present",
        "description": "Led development of microservices architecture..."
      }
    ],
    "education": [
      {
        "degree": "B.S. Computer Science",
        "school": "University of Example",
        "year": "2018"
      }
    ],
    "skills": ["Python", "JavaScript", "React", "Node.js", "PostgreSQL"]
  },
  "status": "completed",
  "created_at": "2024-12-19T10:30:00Z",
  "updated_at": "2024-12-19T10:30:15Z"
}
```

### List Resumes

Get a paginated list of all resumes.

**Endpoint**: `GET /api/v1/resumes/`

**Query Parameters**:
- `skip` (integer, default: 0)
- `limit` (integer, default: 10, max: 100)

**Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/resumes/?skip=0&limit=10"
```

**Response** (200 OK):
```json
{
  "items": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440000",
      "filename": "resume.pdf",
      "status": "completed",
      "created_at": "2024-12-19T10:30:00Z"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "filename": "john_doe_resume.docx",
      "status": "completed",
      "created_at": "2024-12-19T09:00:00Z"
    }
  ],
  "total": 5,
  "skip": 0,
  "limit": 10
}
```

### Get Resume by ID

Retrieve details of a specific resume.

**Endpoint**: `GET /api/v1/resumes/{resume_id}`

**Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/resumes/660e8400-e29b-41d4-a716-446655440000"
```

**Response** (200 OK):
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440000",
  "filename": "resume.pdf",
  "file_path": "resumes/a3b2c1d4e5f6.../resume.pdf",
  "content_hash": "a3b2c1d4e5f67890abcdef1234567890",
  "parsed_content": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-0123",
    "summary": "Experienced software engineer with 5+ years...",
    "experience": [...],
    "education": [...],
    "skills": [...]
  },
  "status": "completed",
  "created_at": "2024-12-19T10:30:00Z",
  "updated_at": "2024-12-19T10:30:15Z"
}
```

### Delete Resume

Delete a resume and all associated files.

**Endpoint**: `DELETE /api/v1/resumes/{resume_id}`

**Request**:
```bash
curl -X DELETE "http://localhost:8000/api/v1/resumes/660e8400-e29b-41d4-a716-446655440000"
```

**Response** (204 No Content)

## Applications API

### Create Application

Create a job application (links a job and resume for processing).

**Endpoint**: `POST /api/v1/applications/`

**Request**:
```bash
curl -X POST "http://localhost:8000/api/v1/applications/" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "550e8400-e29b-41d4-a716-446655440000",
    "resume_id": "660e8400-e29b-41d4-a716-446655440000",
    "notes": "Applying for the backend engineer position"
  }'
```

**Request Body**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "resume_id": "660e8400-e29b-41d4-a716-446655440000",
  "notes": "Applying for the backend engineer position"
}
```

**Response** (201 Created):
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440000",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "resume_id": "660e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "tailored_resume_path": null,
  "cover_letter_path": null,
  "notes": "Applying for the backend engineer position",
  "created_at": "2024-12-19T11:00:00Z",
  "updated_at": "2024-12-19T11:00:00Z",
  "job": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Senior Software Engineer",
    "company": "Example Corp"
  },
  "resume": {
    "id": "660e8400-e29b-41d4-a716-446655440000",
    "filename": "resume.pdf"
  }
}
```

### List Applications

Get a paginated list of all applications.

**Endpoint**: `GET /api/v1/applications/`

**Query Parameters**:
- `skip` (integer, default: 0)
- `limit` (integer, default: 10, max: 100)
- `status` (string, optional): Filter by status

**Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/applications/?skip=0&limit=10&status=completed"
```

**Response** (200 OK):
```json
{
  "items": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440000",
      "job_id": "550e8400-e29b-41d4-a716-446655440000",
      "resume_id": "660e8400-e29b-41d4-a716-446655440000",
      "status": "completed",
      "created_at": "2024-12-19T11:00:00Z",
      "job": {
        "title": "Senior Software Engineer",
        "company": "Example Corp"
      },
      "resume": {
        "filename": "resume.pdf"
      }
    }
  ],
  "total": 3,
  "skip": 0,
  "limit": 10
}
```

### Get Application by ID

Retrieve details of a specific application.

**Endpoint**: `GET /api/v1/applications/{application_id}`

**Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/applications/770e8400-e29b-41d4-a716-446655440000"
```

**Response** (200 OK):
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440000",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "resume_id": "660e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "tailored_resume_path": "tailored/770e8400_resume.docx",
  "tailored_resume_pdf_path": "tailored/770e8400_resume.pdf",
  "cover_letter_path": "cover_letters/770e8400_cover_letter.docx",
  "cover_letter_pdf_path": "cover_letters/770e8400_cover_letter.pdf",
  "notes": "Applying for the backend engineer position",
  "created_at": "2024-12-19T11:00:00Z",
  "updated_at": "2024-12-19T11:02:30Z",
  "job": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Senior Software Engineer",
    "company": "Example Corp",
    "location": "San Francisco, CA"
  },
  "resume": {
    "id": "660e8400-e29b-41d4-a716-446655440000",
    "filename": "resume.pdf"
  }
}
```

### Generate Cover Letter

Generate a cover letter for an existing application.

**Endpoint**: `POST /api/v1/applications/{application_id}/generate-cover-letter`

**Request**:
```bash
curl -X POST "http://localhost:8000/api/v1/applications/770e8400-e29b-41d4-a716-446655440000/generate-cover-letter" \
  -H "Content-Type: application/json" \
  -d '{
    "template": "default",
    "user_details": {
      "name": "John Doe",
      "address": "123 Main St, San Francisco, CA 94102",
      "phone": "+1-555-0123",
      "email": "john.doe@example.com"
    }
  }'
```

**Request Body**:
```json
{
  "template": "default",
  "user_details": {
    "name": "John Doe",
    "address": "123 Main St, San Francisco, CA 94102",
    "phone": "+1-555-0123",
    "email": "john.doe@example.com"
  }
}
```

**Response** (200 OK):
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "cover_letter_path": "cover_letters/770e8400_cover_letter.docx",
  "cover_letter_pdf_path": "cover_letters/770e8400_cover_letter.pdf",
  "download_urls": {
    "docx": "https://storage.example.com/cover_letters/770e8400_cover_letter.docx?signature=...",
    "pdf": "https://storage.example.com/cover_letters/770e8400_cover_letter.pdf?signature=..."
  },
  "updated_at": "2024-12-19T11:05:00Z"
}
```

### Download Application Files

Get presigned URLs for downloading application files.

**Endpoint**: `GET /api/v1/applications/{application_id}/download/{file_type}`

**Path Parameters**:
- `file_type`: One of `resume_docx`, `resume_pdf`, `cover_letter_docx`, `cover_letter_pdf`

**Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/applications/770e8400-e29b-41d4-a716-446655440000/download/resume_pdf"
```

**Response** (200 OK):
```json
{
  "download_url": "https://storage.example.com/tailored/770e8400_resume.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&...",
  "filename": "770e8400_resume.pdf",
  "expires_in": 3600
}
```

### Update Application

Update application details or status.

**Endpoint**: `PUT /api/v1/applications/{application_id}`

**Request**:
```bash
curl -X PUT "http://localhost:8000/api/v1/applications/770e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "notes": "Updated: Submitted application on 12/19/2024",
    "status": "submitted"
  }'
```

**Response** (200 OK):
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440000",
  "status": "submitted",
  "notes": "Updated: Submitted application on 12/19/2024",
  "updated_at": "2024-12-19T12:00:00Z"
}
```

### Delete Application

Delete an application and associated files.

**Endpoint**: `DELETE /api/v1/applications/{application_id}`

**Request**:
```bash
curl -X DELETE "http://localhost:8000/api/v1/applications/770e8400-e29b-41d4-a716-446655440000"
```

**Response** (204 No Content)

## Health Check

### Check API Health

Get the health status of the API.

**Endpoint**: `GET /health`

**Request**:
```bash
curl -X GET "http://localhost:8000/health"
```

**Response** (200 OK):
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "database": "connected",
  "redis": "connected",
  "storage": "available",
  "timestamp": "2024-12-19T12:00:00Z"
}
```

## Error Responses

### Validation Error (422)

**Response**:
```json
{
  "detail": [
    {
      "loc": ["body", "url"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Not Found (404)

**Response**:
```json
{
  "detail": "Job not found"
}
```

### Server Error (500)

**Response**:
```json
{
  "detail": "Internal server error",
  "error_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "An unexpected error occurred. Please contact support with the error ID."
}
```

## Status Codes

| Code | Description | Usage |
|------|-------------|-------|
| 200 | OK | Successful GET, PUT request |
| 201 | Created | Successful POST request |
| 204 | No Content | Successful DELETE request |
| 400 | Bad Request | Invalid request format |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Service temporarily unavailable |

## Rate Limiting (Future)

Rate limiting will be implemented in future versions:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

## Pagination

All list endpoints support pagination with these query parameters:

- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 10, max: 100)

Response includes pagination metadata:

```json
{
  "items": [...],
  "total": 100,
  "skip": 0,
  "limit": 10
}
```

## Testing the API

### Using Swagger UI

Visit `http://localhost:8000/docs` for interactive API documentation.

### Using curl

All examples in this document use curl commands.

### Using Postman

Import the API into Postman:
1. Go to `http://localhost:8000/openapi.json`
2. Copy the JSON
3. Import into Postman

### Using Python

```python
import requests

# Create a job
response = requests.post(
    "http://localhost:8000/api/v1/jobs/",
    json={"url": "https://example.com/jobs/software-engineer"}
)
job = response.json()
print(job)

# Upload a resume
with open("resume.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/v1/resumes/upload",
        files={"file": f}
    )
resume = response.json()
print(resume)

# Create an application
response = requests.post(
    "http://localhost:8000/api/v1/applications/",
    json={
        "job_id": job["id"],
        "resume_id": resume["id"]
    }
)
application = response.json()
print(application)
```

### Using JavaScript/TypeScript

```typescript
// Create a job
const createJob = async (url: string) => {
  const response = await fetch('http://localhost:8000/api/v1/jobs/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url }),
  });
  return response.json();
};

// Upload a resume
const uploadResume = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('http://localhost:8000/api/v1/resumes/upload', {
    method: 'POST',
    body: formData,
  });
  return response.json();
};

// Create an application
const createApplication = async (jobId: string, resumeId: string) => {
  const response = await fetch('http://localhost:8000/api/v1/applications/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ job_id: jobId, resume_id: resumeId }),
  });
  return response.json();
};
```

---

**Last Updated**: 2024-12-19  
**API Version**: v1  
**Document Version**: 1.0
