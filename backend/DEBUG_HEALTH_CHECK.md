# Debugging Railway Health Check Failures

This guide helps you resolve the specific "Healthcheck failed!" issue you're experiencing.

## Current Issue
- Railway shows "Service unavailable" for health checks
- Application appears to not be starting properly
- Health check timeout after multiple retries

## Step-by-Step Debugging

### 1. Check Railway Logs First

**Most Important**: Check the Railway deployment logs to see what's actually happening:

1. Go to Railway Dashboard
2. Click on your service
3. Go to "Deployments" tab
4. Click on the latest deployment
5. Look at the logs for:
   - Import errors
   - Missing dependencies
   - Database connection errors
   - Port binding issues

### 2. Test Locally First

Before deploying to Railway, test locally:

```bash
cd backend

# Test basic startup
python test_startup.py

# Test with uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Test health endpoint
curl http://localhost:8000/health
```

### 3. Check Environment Variables

Ensure these are set in Railway:

```bash
# Required (Railway should provide these automatically)
DATABASE_URL=postgresql://...
REDIS_URL=redis://...

# Optional but recommended
ENVIRONMENT=production
DEBUG=false
BACKEND_CORS_ORIGINS=https://your-frontend.vercel.app
```

### 4. Common Causes and Solutions

#### A. Missing Dependencies
**Symptoms**: Import errors in logs
**Solution**: Check `requirements.txt` includes all needed packages

#### B. Database Connection Issues
**Symptoms**: Database connection errors
**Solution**: 
- Verify PostgreSQL service is running in Railway
- Check `DATABASE_URL` format
- The app now starts without requiring DB connection

#### C. Port Binding Issues
**Symptoms**: "Address already in use" or port errors
**Solution**: 
- Railway provides `$PORT` environment variable
- App should bind to `0.0.0.0:$PORT`

#### D. File System Issues
**Symptoms**: Permission errors or file creation failures
**Solution**: 
- Removed file logging (now only uses stdout)
- Simplified startup process

### 5. Alternative Startup Methods

If the current startup fails, try these alternatives:

#### Option A: Use Procfile (Railway fallback)
Railway will use the Procfile if `railway.json` fails:
```bash
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1 --log-level info
```

#### Option B: Direct uvicorn command
Update `railway.json`:
```json
{
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1 --log-level info",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 180
  }
}
```

#### Option C: Simple Python script
Create `simple_start.py`:
```python
import os
import uvicorn
from app.main import app

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8000))
    uvicorn.run(app, host='0.0.0.0', port=port, workers=1)
```

### 6. Health Check Troubleshooting

#### A. Test Health Endpoint Manually
Once the app is running, test the health endpoint:
```bash
curl https://your-app.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "LaudatorAI API",
  "timestamp": 1234567890.123,
  "version": "0.1.0"
}
```

#### B. Health Check Configuration
Current health check settings:
- **Path**: `/health`
- **Timeout**: 180 seconds
- **Retries**: 5 attempts

#### C. Health Check Logic
The health endpoint now:
- Returns immediately (no database check)
- Always returns HTTP 200
- Includes basic service information

### 7. Emergency Fixes

#### A. Rollback to Working Version
1. Go to Railway Dashboard
2. Find a working deployment
3. Click "Redeploy"

#### B. Recreate Service
If all else fails:
1. Create new Railway service
2. Connect to same GitHub repo
3. Add PostgreSQL and Redis services
4. Set environment variables
5. Deploy

#### C. Use Railway CLI for Debugging
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and link
railway login
railway link

# Check logs
railway logs

# Deploy manually
railway up
```

### 8. Monitoring and Verification

#### A. Check Service Status
1. Railway Dashboard → Service → Overview
2. Look for:
   - Service status (Running/Stopped)
   - Resource usage
   - Recent deployments

#### B. Verify Endpoints
Once running, test these endpoints:
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /docs` - API documentation

#### C. Check External Services
- PostgreSQL service status
- Redis service status
- Network connectivity

### 9. Next Steps After Fix

Once the health check passes:

1. **Add Database Check**: Re-enable database connectivity test in health endpoint
2. **Add Monitoring**: Set up proper logging and monitoring
3. **Optimize**: Fine-tune performance and resource usage
4. **Test Integration**: Verify frontend can connect to backend

### 10. Getting Help

If you're still stuck:

1. **Share Logs**: Copy the Railway deployment logs
2. **Test Locally**: Run `python test_startup.py` and share results
3. **Check Dependencies**: Verify all packages are in `requirements.txt`
4. **Railway Support**: Use Railway's support channels

## Quick Checklist

- [ ] Check Railway deployment logs
- [ ] Test application locally
- [ ] Verify environment variables
- [ ] Check PostgreSQL service is running
- [ ] Test health endpoint manually
- [ ] Try alternative startup methods
- [ ] Verify all dependencies are installed
