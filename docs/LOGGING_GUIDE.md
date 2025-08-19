# LaudatorAI Logging Guide

This guide explains the comprehensive logging system implemented for both frontend and backend to ensure robust monitoring and debugging capabilities.

## Overview

The logging system provides:
- **Structured JSON logging** for production environments
- **Human-readable logging** for development
- **Frontend-to-backend log forwarding** for centralized monitoring
- **Error tracking** with full stack traces
- **Performance monitoring** with timing measurements
- **Security event logging** for audit trails
- **User action tracking** for analytics

## Backend Logging

### Configuration

The backend uses a custom logging system located in `backend/app/core/logging.py`:

- **JSON Formatter**: Structured logging for production environments
- **File Logging**: Local log files for development
- **Console Logging**: stdout for Railway/Vercel compatibility
- **Structured Data**: Request IDs, user context, performance metrics

### Key Features

#### 1. Request Logging
```python
# Automatic request logging with middleware
log_request(
    request_id="uuid",
    method="GET",
    path="/api/v1/jobs",
    status_code=200,
    duration=0.123,
    ip_address="192.168.1.1",
    user_agent="Mozilla/5.0..."
)
```

#### 2. API Call Logging
```python
log_api_call(
    api_name="job_extraction",
    method="POST",
    endpoint="/api/v1/jobs/extract",
    status_code=200,
    duration=1.234,
    request_id="uuid",
    user_id="user123"
)
```

#### 3. Task Logging
```python
log_task_start(task_id="task123", task_type="resume_processing")
log_task_complete(task_id="task123", task_type="resume_processing", duration=5.67)
log_task_error(task_id="task123", task_type="resume_processing", error="File not found")
```

#### 4. Database Operations
```python
log_database_operation(
    operation="SELECT",
    table="jobs",
    success=True,
    duration=0.045
)
```

#### 5. External API Calls
```python
log_external_api_call(
    service="openai",
    endpoint="/v1/chat/completions",
    method="POST",
    status_code=200,
    duration=2.34
)
```

#### 6. Security Events
```python
log_security_event(
    event_type="authentication_failure",
    severity="medium",
    details="Invalid credentials for user@example.com"
)
```

### Environment Configuration

- **Development**: Human-readable logs to console and file
- **Production**: JSON-structured logs to stdout (Railway/Vercel compatible)

## Frontend Logging

### Configuration

The frontend uses `loglevel` with custom structured logging located in `frontend/src/lib/logger.ts`:

- **Remote Logging**: Sends logs to backend in production
- **Session Tracking**: Unique session IDs for user tracking
- **Performance Monitoring**: Built-in timing measurements
- **Error Boundaries**: React error catching and logging

### Key Features

#### 1. Basic Logging
```typescript
import { logger } from '@/lib/logger';

logger.info('User logged in', { userId: 'user123' });
logger.warn('API rate limit approaching', { endpoint: '/api/jobs' });
logger.error('Failed to upload file', error, { fileName: 'resume.pdf' });
```

#### 2. Specialized Loggers
```typescript
import { apiLogger, uiLogger, performanceLogger } from '@/lib/logger';

// API-specific logging
apiLogger.logApiCall('GET', '/api/jobs', 200, 150);

// UI-specific logging
uiLogger.logUserAction('click', 'submit_button', true);

// Performance logging
performanceLogger.logPerformance('page_load', 1200, 'ms');
```

#### 3. Utility Functions
```typescript
import { logUtils } from '@/lib/logger';

// Component lifecycle
logUtils.logComponentMount('JobForm', { hasResume: true });
logUtils.logComponentUnmount('JobForm');

// Form interactions
logUtils.logFormSubmit('job_application', true, { jobId: '123' });
logUtils.logFormValidation('job_application', { title: 'Required' });

// File operations
logUtils.logFileUpload('resume.pdf', 1024000, true);
logUtils.logFileDownload('cover_letter.pdf', true);

// Navigation
logUtils.logNavigation('/jobs', '/application', 'link');
```

#### 4. Performance Monitoring
```typescript
import { measurePerformance, measureAsyncPerformance } from '@/lib/logger';

// Synchronous performance measurement
const result = measurePerformance('data_processing', () => {
  return processData(largeDataset);
});

// Asynchronous performance measurement
const result = await measureAsyncPerformance('api_call', async () => {
  return await apiClient.createApplication(jobId, resumeId);
});
```

#### 5. Error Boundary Integration
```typescript
// Automatic error logging in React components
<ErrorBoundary>
  <YourComponent />
</ErrorBoundary>
```

### Remote Logging

In production, frontend logs are automatically sent to the backend via:
1. **Frontend API Route**: `/api/logs` (Next.js API route)
2. **Backend Endpoint**: `/api/v1/logs` (FastAPI endpoint)
3. **Fallback**: Console logging if backend is unavailable

## Log Structure

### Backend Log Format (Production)
```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "INFO",
  "logger": "laudatorai.api",
  "message": "HTTP Request | GET /api/v1/jobs | 200 | 0.123s",
  "module": "main",
  "function": "add_process_time_header",
  "line": 67,
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "method": "GET",
  "path": "/api/v1/jobs",
  "status_code": 200,
  "duration": 0.123,
  "ip_address": "192.168.1.1",
  "user_agent": "Mozilla/5.0..."
}
```

### Frontend Log Format (Production)
```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "INFO",
  "logger": "LaudatorAI.API",
  "message": "API Call | GET /api/v1/jobs | 200 | 150ms",
  "sessionId": "session_1705315845123_abc123def",
  "url": "https://laudator-ai.vercel.app/",
  "data": {
    "method": "GET",
    "endpoint": "/api/v1/jobs",
    "status": 200,
    "duration": 150
  }
}
```

## Monitoring and Debugging

### Vercel Logs

Frontend logs appear in Vercel's function logs:
```bash
# View Vercel logs
vercel logs --follow
```

### Railway Logs

Backend logs appear in Railway's application logs:
```bash
# View Railway logs
railway logs
```

### Local Development

#### Backend Logs
```bash
# View backend logs
tail -f backend/logs/app.log
```

#### Frontend Logs
- Open browser DevTools → Console
- All logs are visible in development mode

### Log Levels

- **DEBUG**: Detailed debugging information
- **INFO**: General application flow
- **WARN**: Warning conditions
- **ERROR**: Error conditions with stack traces

### Environment Variables

#### Frontend
```env
NODE_ENV=production
BACKEND_API_URL=https://your-backend.railway.app
```

#### Backend
```env
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
```

## Best Practices

### 1. Log Sensitive Information
- ❌ Never log passwords, API keys, or personal data
- ✅ Log user actions, errors, and performance metrics
- ✅ Use structured data for better filtering

### 2. Performance Considerations
- Use appropriate log levels
- Avoid logging in tight loops
- Use async logging for non-critical operations

### 3. Error Handling
- Always include context with errors
- Use structured error logging
- Include stack traces for debugging

### 4. Monitoring
- Set up alerts for ERROR level logs
- Monitor performance metrics
- Track user actions for analytics

## Troubleshooting

### No Frontend Logs in Vercel
1. Check if `BACKEND_API_URL` is set correctly
2. Verify the `/api/logs` endpoint is working
3. Check browser console for errors

### No Backend Logs in Railway
1. Ensure logs are going to stdout
2. Check environment variables
3. Verify logging configuration

### Performance Issues
1. Check log levels (too much DEBUG logging)
2. Monitor log volume
3. Use performance measurements to identify bottlenecks

## Integration with External Services

The logging system can be easily extended to integrate with:
- **Sentry**: Error tracking and monitoring
- **DataDog**: Application performance monitoring
- **LogRocket**: Session replay and debugging
- **Google Analytics**: User behavior tracking

## Security Considerations

- All logs are sanitized to remove sensitive data
- IP addresses are logged for security monitoring
- User agents are logged for debugging
- Session IDs are used for user tracking without PII
