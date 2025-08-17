# Railway Deployment Troubleshooting Guide

This guide helps you resolve common issues when deploying the LaudatorAI backend to Railway.

## Common Issues and Solutions

### 1. Health Check Failures

**Symptoms:**
- Railway shows "Healthcheck failed!"
- Service unavailable errors
- Application not starting

**Solutions:**

#### A. Check Environment Variables
Ensure these environment variables are set in Railway:
```bash
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
BACKEND_CORS_ORIGINS=https://your-frontend.vercel.app
```

#### B. Check Database Connection
The health check now tests database connectivity. If the database is not accessible:
- Verify PostgreSQL service is running in Railway
- Check `DATABASE_URL` format
- Ensure database is not in maintenance mode

#### C. Check Application Logs
1. Go to Railway Dashboard
2. Click on your service
3. Go to "Deployments" tab
4. Click on the latest deployment
5. Check the logs for errors

### 2. Application Startup Issues

**Symptoms:**
- Application fails to start
- Import errors
- Missing dependencies

**Solutions:**

#### A. Check Requirements
Ensure all dependencies are in `requirements.txt`:
```bash
fastapi==0.116.1
uvicorn[standard]==0.35.0
sqlalchemy==2.0.43
alembic==1.14.0
psycopg2-binary==2.9.10
redis==5.2.0
celery==5.5.3
```

#### B. Check Python Version
The application requires Python 3.11+. Railway should automatically detect this.

#### C. Check Build Process
1. Monitor the build logs in Railway
2. Look for any failed pip install commands
3. Check for missing system dependencies

### 3. Database Migration Issues

**Symptoms:**
- Database tables not created
- Migration errors
- Connection timeouts

**Solutions:**

#### A. Manual Migration
If automatic migrations fail, you can run them manually:
1. Go to Railway Dashboard
2. Click on your service
3. Go to "Variables" tab
4. Add a temporary variable: `RUN_MIGRATIONS=true`
5. Redeploy the service

#### B. Check Database URL
Ensure the `DATABASE_URL` is in the correct format:
```
postgresql://username:password@host:port/database
```

#### C. Database Permissions
Ensure the database user has the necessary permissions:
- CREATE TABLE
- INSERT, SELECT, UPDATE, DELETE
- CREATE INDEX

### 4. Port and Host Issues

**Symptoms:**
- Application not accessible
- Connection refused errors
- Wrong port binding

**Solutions:**

#### A. Check Port Configuration
Railway automatically provides the `PORT` environment variable. The application should bind to:
```python
port = int(os.getenv('PORT', 8000))
host = '0.0.0.0'  # Important: bind to all interfaces
```

#### B. Check Railway Configuration
Ensure `railway.json` has the correct settings:
```json
{
  "deploy": {
    "startCommand": "python start.py",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 120
  }
}
```

### 5. Memory and Resource Issues

**Symptoms:**
- Application crashes
- Out of memory errors
- Slow performance

**Solutions:**

#### A. Check Resource Usage
1. Go to Railway Dashboard
2. Monitor CPU and memory usage
3. Consider upgrading the service plan if needed

#### B. Optimize Application
- Use single worker mode (`--workers 1`)
- Implement connection pooling
- Add caching where appropriate

### 6. CORS Issues

**Symptoms:**
- Frontend can't connect to backend
- CORS errors in browser console
- API requests blocked

**Solutions:**

#### A. Update CORS Configuration
Set the correct frontend URL in Railway environment variables:
```bash
BACKEND_CORS_ORIGINS=https://your-frontend.vercel.app
```

#### B. Check Multiple Origins
If you have multiple frontend URLs, separate them with commas:
```bash
BACKEND_CORS_ORIGINS=https://app1.vercel.app,https://app2.vercel.app
```

## Debugging Steps

### 1. Check Application Logs
```bash
# In Railway Dashboard
# Go to your service → Deployments → Latest deployment → Logs
```

### 2. Test Health Endpoint Locally
```bash
# Test the health endpoint
curl http://localhost:8000/health
```

### 3. Check Environment Variables
```bash
# In Railway Dashboard
# Go to your service → Variables
# Ensure all required variables are set
```

### 4. Test Database Connection
```bash
# You can test the database connection using Railway's shell
# Go to your service → Deployments → Latest deployment → Shell
psql $DATABASE_URL -c "SELECT 1;"
```

### 5. Check Redis Connection
```bash
# Test Redis connection
redis-cli -u $REDIS_URL ping
```

## Emergency Recovery

### 1. Rollback to Previous Deployment
1. Go to Railway Dashboard
2. Click on your service
3. Go to "Deployments" tab
4. Find a working deployment
5. Click "Redeploy"

### 2. Reset Environment Variables
1. Go to Railway Dashboard
2. Click on your service
3. Go to "Variables" tab
4. Reset to default values
5. Redeploy

### 3. Recreate Service
If all else fails:
1. Create a new Railway service
2. Connect to the same GitHub repository
3. Configure environment variables
4. Deploy

## Monitoring and Alerts

### 1. Set Up Monitoring
- Monitor the `/health` endpoint
- Set up alerts for failed deployments
- Monitor resource usage

### 2. Log Analysis
- Use Railway's built-in log viewer
- Set up external logging (e.g., Sentry)
- Monitor error rates

### 3. Performance Monitoring
- Monitor response times
- Track database query performance
- Monitor memory usage

## Best Practices

### 1. Environment Management
- Use different environments for dev/staging/prod
- Never commit secrets to the repository
- Use Railway's secret management

### 2. Deployment Strategy
- Test locally before deploying
- Use feature branches for development
- Monitor deployments closely

### 3. Database Management
- Use migrations for schema changes
- Backup data regularly
- Monitor database performance

### 4. Security
- Use HTTPS in production
- Validate all inputs
- Implement rate limiting
- Regular security updates

## Getting Help

If you're still experiencing issues:

1. **Check Railway Documentation**: https://docs.railway.app
2. **Review Application Logs**: Look for specific error messages
3. **Test Locally**: Ensure the application works locally
4. **Contact Support**: Use Railway's support channels

## Common Error Messages

### "Service unavailable"
- Check if the application is starting properly
- Verify environment variables
- Check database connectivity

### "Connection refused"
- Verify the application is binding to the correct port
- Check Railway's port configuration
- Ensure the service is running

### "Database connection failed"
- Verify `DATABASE_URL` is correct
- Check if PostgreSQL service is running
- Ensure database permissions

### "Import error"
- Check if all dependencies are in `requirements.txt`
- Verify Python version compatibility
- Check for missing system dependencies
