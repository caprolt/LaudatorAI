# Railway Deployment Troubleshooting Guide

## Common Issues and Solutions

### 1. 502 Bad Gateway Error

**Symptoms**: Backend returns 502 Bad Gateway when accessed
**Causes**: Application failing to start, missing dependencies, environment variable issues

**Solutions**:

#### Check Railway Logs
1. Go to your Railway project dashboard
2. Click on your backend service
3. Go to "Deployments" tab
4. Click on the latest deployment
5. Check the logs for error messages

#### Verify Environment Variables
Ensure these environment variables are set in Railway:

```bash
# Required for Railway
DATABASE_URL=postgresql://...
REDIS_URL=redis://...

# CORS Configuration (add your frontend domain)
BACKEND_CORS_ORIGINS=https://your-frontend-domain.vercel.app,http://localhost:3000

# Optional but recommended
ENVIRONMENT=production
DEBUG=false
OPENAI_API_KEY=your-openai-key
```

#### Check Application Startup
The application should start with the command specified in `railway.json`:
```json
{
  "deploy": {
    "startCommand": "python start.py"
  }
}
```

### 2. CORS Issues

**Symptoms**: Frontend can't connect to backend, CORS errors in browser console

**Solutions**:

#### Update CORS Configuration
1. In Railway dashboard, go to your backend service
2. Go to "Variables" tab
3. Add/update `BACKEND_CORS_ORIGINS`:
   ```
   BACKEND_CORS_ORIGINS=https://your-frontend-domain.vercel.app,http://localhost:3000
   ```

#### Verify CORS in Code
The CORS configuration is in `app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Database Connection Issues

**Symptoms**: Application fails to start, database connection errors

**Solutions**:

#### Check Database URL
1. Ensure `DATABASE_URL` is set in Railway
2. Format should be: `postgresql://username:password@host:port/database`
3. Railway automatically provides this when you add a PostgreSQL service

#### Test Database Connection
Add this to your `start.py` for debugging:
```python
import os
print(f"DATABASE_URL: {os.getenv('DATABASE_URL', 'NOT SET')}")
```

### 4. Redis Connection Issues

**Symptoms**: Celery tasks failing, Redis connection errors

**Solutions**:

#### Check Redis URL
1. Ensure `REDIS_URL` is set in Railway
2. Format should be: `redis://username:password@host:port/database`
3. Railway automatically provides this when you add a Redis service

### 5. Build Issues

**Symptoms**: Deployment fails during build phase

**Solutions**:

#### Check Requirements
Ensure all dependencies are in `requirements.txt`:
```bash
# Core dependencies
fastapi==0.116.1
uvicorn[standard]==0.35.0
pydantic==2.11.7
pydantic-settings==2.10.1
sqlalchemy==2.0.43
alembic==1.14.0
psycopg2-binary==2.9.10
redis==5.2.0
celery==5.5.3
```

#### Check Python Version
Ensure `pyproject.toml` specifies Python 3.11+:
```toml
[project]
requires-python = ">=3.11"
```

### 6. Health Check Issues

**Symptoms**: Railway health checks failing

**Solutions**:

#### Verify Health Endpoint
The health endpoint is at `/health` and should return:
```json
{
  "status": "healthy",
  "service": "LaudatorAI API",
  "timestamp": 1234567890,
  "version": "0.1.0"
}
```

#### Update Railway Configuration
Ensure `railway.json` has correct health check path:
```json
{
  "deploy": {
    "healthcheckPath": "/health",
    "healthcheckTimeout": 180
  }
}
```

## Debugging Steps

### 1. Check Railway Logs
```bash
# View recent logs
railway logs

# Follow logs in real-time
railway logs --follow
```

### 2. Test Locally with Railway Environment
```bash
# Get Railway environment variables
railway variables

# Test locally with Railway env
railway run python start.py
```

### 3. Verify Service Dependencies
Ensure your backend service depends on:
- PostgreSQL service
- Redis service

### 4. Check Resource Limits
Railway has resource limits. Check if your app is hitting them:
- CPU usage
- Memory usage
- Disk space

## Quick Fix Checklist

- [ ] Check Railway logs for specific error messages
- [ ] Verify all environment variables are set
- [ ] Ensure DATABASE_URL and REDIS_URL are correct
- [ ] Update BACKEND_CORS_ORIGINS with your frontend domain
- [ ] Verify the application starts locally with Railway environment
- [ ] Check that all required services (PostgreSQL, Redis) are running
- [ ] Ensure health endpoint `/health` is accessible
- [ ] Verify build process completes successfully

## Emergency Rollback

If deployment is completely broken:

1. Go to Railway dashboard
2. Click on your backend service
3. Go to "Deployments" tab
4. Find the last working deployment
5. Click "Redeploy" on that deployment

## Contact Support

If issues persist:
1. Collect logs from Railway dashboard
2. Note the specific error messages
3. Check this troubleshooting guide
4. Contact Railway support with detailed information
