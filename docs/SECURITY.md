# Security & Best Practices

This document outlines the security measures, best practices, and design decisions implemented in LaudatorAI.

## Table of Contents

- [Security Architecture](#security-architecture)
- [Input Validation](#input-validation)
- [File Upload Security](#file-upload-security)
- [Database Security](#database-security)
- [API Security](#api-security)
- [Authentication & Authorization](#authentication--authorization-future)
- [Data Privacy](#data-privacy)
- [Dependency Management](#dependency-management)
- [Best Practices](#best-practices)
- [Security Checklist](#security-checklist)
- [Reporting Security Issues](#reporting-security-issues)

## Security Architecture

### Defense in Depth

LaudatorAI implements multiple layers of security:

1. **Input Layer**: Validation and sanitization
2. **Application Layer**: Authentication and authorization
3. **Data Layer**: Encrypted storage and secure queries
4. **Network Layer**: HTTPS, CORS, rate limiting
5. **Infrastructure Layer**: Container isolation, secrets management

### Security Principles

- **Least Privilege**: Services have minimal permissions
- **Fail Securely**: Errors don't expose sensitive information
- **Secure by Default**: Security features enabled out of the box
- **Defense in Depth**: Multiple security layers
- **Separation of Concerns**: Clear boundaries between components

## Input Validation

### Pydantic Validation

All API inputs are validated using Pydantic schemas:

```python
from pydantic import BaseModel, HttpUrl, validator
from typing import Optional

class JobCreate(BaseModel):
    url: HttpUrl  # Validates URL format
    
    @validator('url')
    def validate_url_scheme(cls, v):
        if v.scheme not in ['http', 'https']:
            raise ValueError('Only HTTP(S) URLs are allowed')
        return v
```

### SQL Injection Prevention

SQLAlchemy ORM uses parameterized queries:

```python
# ✅ Safe - Parameterized query
job = db.query(Job).filter(Job.id == job_id).first()

# ❌ Never do this
query = f"SELECT * FROM jobs WHERE id = '{job_id}'"  # Vulnerable!
```

### XSS Prevention

- All user inputs are escaped in responses
- Content-Type headers properly set
- Output encoding in templates

## File Upload Security

### File Type Validation

```python
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.doc'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def validate_file(file: UploadFile):
    # Check extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"File type {ext} not allowed")
    
    # Check file size
    file.file.seek(0, 2)  # Seek to end
    size = file.file.tell()
    file.file.seek(0)  # Reset
    
    if size > MAX_FILE_SIZE:
        raise ValueError(f"File size exceeds {MAX_FILE_SIZE} bytes")
    
    return True
```

### File Storage Security

1. **Content Hashing**: SHA256 hash prevents duplicates
2. **Unique Filenames**: UUID-based names prevent collisions
3. **Presigned URLs**: Time-limited access to files
4. **Virus Scanning**: (Future) ClamAV integration
5. **Access Control**: Files stored in private buckets

```python
import hashlib

def hash_file_content(content: bytes) -> str:
    """Generate SHA256 hash of file content."""
    return hashlib.sha256(content).hexdigest()
```

### File Path Traversal Prevention

```python
import os
from pathlib import Path

def safe_join(directory: str, filename: str) -> str:
    """Safely join directory and filename."""
    # Resolve paths to absolute
    base = Path(directory).resolve()
    target = (base / filename).resolve()
    
    # Ensure target is within base directory
    if not str(target).startswith(str(base)):
        raise ValueError("Path traversal detected")
    
    return str(target)
```

## Database Security

### Connection Security

```python
# Use environment variables for credentials
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost/db"
)

# SSL mode for production
if settings.ENVIRONMENT == "production":
    DATABASE_URL += "?sslmode=require"
```

### Password Storage (Future)

When user authentication is implemented:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

### Sensitive Data

- API keys stored in environment variables
- Secrets never committed to repository
- Database credentials in secure secrets manager
- `.env` files excluded from version control

## API Security

### CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,  # From env
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

### Rate Limiting (Future)

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/jobs/")
@limiter.limit("10/minute")
async def create_job(request: Request, job: JobCreate):
    # Endpoint implementation
    pass
```

### Request Validation

- All requests validated via Pydantic
- File uploads size-limited
- Request timeout configured
- Body size limits enforced

### Error Handling

```python
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # Log full error for debugging
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    # Return generic error to client
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_id": generate_error_id(),  # For support reference
        }
    )
```

## Authentication & Authorization (Future)

### JWT Token Implementation

```python
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### API Key Authentication

```python
from fastapi import Security
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key
```

## Data Privacy

### PII Handling

1. **Minimize Collection**: Only collect necessary data
2. **Encrypt at Rest**: Database encryption enabled
3. **Encrypt in Transit**: HTTPS enforced
4. **Data Retention**: Automatic cleanup of old data
5. **User Control**: Users can delete their data

### Logging Security

```python
import logging

# ❌ Don't log sensitive data
logger.info(f"User {email} logged in with password {password}")

# ✅ Log safely
logger.info(f"User login attempt", extra={
    "user_id": user_id,
    "ip_address": request.client.host,
    "success": True
})
```

### Data Masking

```python
def mask_email(email: str) -> str:
    """Mask email for logging."""
    username, domain = email.split('@')
    return f"{username[:2]}***@{domain}"

# Example: john.doe@example.com -> jo***@example.com
```

## Dependency Management

### Vulnerability Scanning

```bash
# Check for known vulnerabilities
pip-audit

# Or use safety
safety check -r requirements.txt
```

### Dependency Updates

```bash
# Update dependencies
pip list --outdated
pip install --upgrade <package>

# Update requirements.txt
pip freeze > requirements.txt
```

### Pinned Versions

```txt
# requirements.txt
fastapi==0.104.1  # Pinned to specific version
pydantic>=2.0.0,<3.0.0  # Version range
```

## Best Practices

### Code Review Checklist

- [ ] All inputs validated
- [ ] No sensitive data in logs
- [ ] Error messages don't expose internals
- [ ] SQL queries use ORM or parameterized
- [ ] File uploads validated and size-limited
- [ ] HTTPS enforced in production
- [ ] Secrets in environment variables
- [ ] Dependencies up to date
- [ ] Tests include security scenarios

### Secure Configuration

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Security settings
    SECRET_KEY: str
    API_KEY: str
    
    # Database
    DATABASE_URL: str
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    
    # Environment
    ENVIRONMENT: str = "development"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
```

### Environment Variables

```bash
# .env (never commit this file)
SECRET_KEY=your-secret-key-here-generate-with-openssl
API_KEY=your-api-key-here
DATABASE_URL=postgresql://user:pass@localhost/db
BACKEND_CORS_ORIGINS=["https://yourfrontend.com"]
ENVIRONMENT=production
```

Generate secure secrets:
```bash
# Generate SECRET_KEY
openssl rand -hex 32

# Generate API_KEY
openssl rand -base64 32
```

### Production Deployment

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  backend:
    environment:
      - ENVIRONMENT=production
      - LOG_LEVEL=WARNING
    secrets:
      - db_password
      - secret_key
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G

secrets:
  db_password:
    external: true
  secret_key:
    external: true
```

## Security Checklist

### Development

- [x] Input validation with Pydantic
- [x] SQL injection prevention (SQLAlchemy ORM)
- [x] File upload validation
- [x] Error handling (no stack traces in response)
- [x] Logging without sensitive data
- [x] CORS configuration
- [ ] Rate limiting (planned)
- [ ] Authentication (planned)
- [ ] Authorization (planned)

### Deployment

- [ ] HTTPS enforced
- [ ] Security headers configured
- [ ] Database encryption at rest
- [ ] Secrets in secure storage
- [ ] Regular dependency updates
- [ ] Automated security scanning
- [ ] Backup and disaster recovery
- [ ] Monitoring and alerting

### Compliance

- [ ] GDPR compliance (for EU users)
- [ ] Data retention policies
- [ ] Privacy policy
- [ ] Terms of service
- [ ] Cookie consent (if applicable)

## Security Headers

Recommended security headers for production:

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

# Force HTTPS
app.add_middleware(HTTPSRedirectMiddleware)

# Restrict hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
)

# Add security headers
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response
```

## Monitoring & Alerting

### Security Monitoring

```python
import logging
from datetime import datetime

security_logger = logging.getLogger("security")

def log_security_event(event_type: str, details: dict):
    """Log security-related events."""
    security_logger.warning(
        f"Security event: {event_type}",
        extra={
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "details": details
        }
    )

# Examples
log_security_event("invalid_token", {"user_id": user_id})
log_security_event("rate_limit_exceeded", {"ip": request.client.host})
log_security_event("file_upload_rejected", {"filename": filename, "reason": "invalid_type"})
```

### Alerts

Set up alerts for:
- Multiple failed authentication attempts
- Unusual API usage patterns
- File upload rejections
- Database connection failures
- High error rates

## Reporting Security Issues

### Responsible Disclosure

If you discover a security vulnerability:

1. **DO NOT** open a public GitHub issue
2. Email security concerns to: [security@example.com]
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response Timeline

- **24 hours**: Initial acknowledgment
- **7 days**: Preliminary assessment
- **30 days**: Fix developed and deployed
- **After fix**: Public disclosure (with credit)

## Security Resources

### Tools

- **OWASP ZAP**: Security testing
- **Bandit**: Python security linter
- **Safety**: Dependency vulnerability scanner
- **pip-audit**: Python package auditing

### Documentation

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security.html)

---

**Last Updated**: 2024-12-19  
**Document Version**: 1.0  
**Review Schedule**: Quarterly
