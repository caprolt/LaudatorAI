# Railway Deployment Guide for LaudatorAI Backend

This guide will help you deploy the LaudatorAI backend to Railway.

## Prerequisites

1. A Railway account (https://railway.app)
2. GitHub repository with your code
3. Railway CLI (optional but recommended)

## Step 1: Connect Your Repository

1. Go to Railway Dashboard
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Select the `backend` directory as the source

## Step 2: Set Up Environment Variables

In your Railway project dashboard, go to the "Variables" tab and add the following environment variables:

### Required Variables

```bash
# Database (Railway will provide DATABASE_URL automatically)
DATABASE_URL=postgresql://...

# Redis (if using Railway Redis plugin)
REDIS_URL=redis://...

# CORS Origins (add your frontend URL)
BACKEND_CORS_ORIGINS=https://your-frontend-domain.vercel.app

# File Storage (MinIO/S3)
MINIO_ENDPOINT=your-minio-endpoint
MINIO_ACCESS_KEY=your-access-key
MINIO_SECRET_KEY=your-secret-key
MINIO_BUCKET_NAME=laudatorai
MINIO_SECURE=true

# AI/LLM Configuration
OPENAI_API_KEY=your-openai-api-key
LLM_PROVIDER=openai

# Environment
ENVIRONMENT=production
DEBUG=false
```

### Optional Variables

```bash
# Sentry for error tracking
SENTRY_DSN=your-sentry-dsn

# Custom API settings
API_V1_STR=/api/v1
PROJECT_NAME=LaudatorAI
```

## Step 3: Add Required Services

### PostgreSQL Database

1. In your Railway project, click "New Service"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically provide the `DATABASE_URL` environment variable

### Redis (for Celery)

1. In your Railway project, click "New Service"
2. Select "Database" → "Redis"
3. Railway will automatically provide the `REDIS_URL` environment variable

### MinIO/S3 Storage

You have several options:

#### Option A: Use Railway's S3-compatible storage
1. Add a MinIO service to your Railway project
2. Configure the MINIO_* environment variables

#### Option B: Use external S3
1. Use AWS S3 or any S3-compatible service
2. Set the MINIO_* environment variables accordingly

## Step 4: Deploy

1. Railway will automatically deploy when you push to your main branch
2. Monitor the deployment logs in the Railway dashboard
3. Check the health endpoint: `https://your-app.railway.app/health`

## Step 5: Configure Domains

1. In your Railway project, go to "Settings" → "Domains"
2. Add a custom domain or use the provided Railway domain
3. Update your frontend CORS configuration with the new backend URL

## Step 6: Set Up Background Workers (Optional)

For Celery background tasks, you can:

1. Create a separate Railway service for the worker
2. Use the same codebase but with a different start command
3. Set the start command to: `python scripts/start_celery_worker.py`

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Ensure `DATABASE_URL` is properly set
   - Check that the PostgreSQL service is running

2. **Redis Connection Errors**
   - Ensure `REDIS_URL` is properly set
   - Verify Redis service is running

3. **CORS Errors**
   - Update `BACKEND_CORS_ORIGINS` with your frontend URL
   - Include both HTTP and HTTPS versions if needed

4. **File Upload Issues**
   - Verify MinIO/S3 configuration
   - Check bucket permissions

### Logs and Monitoring

1. View logs in the Railway dashboard
2. Set up Sentry for error tracking
3. Monitor the `/health` endpoint

## Environment-Specific Configurations

### Development
```bash
ENVIRONMENT=development
DEBUG=true
```

### Production
```bash
ENVIRONMENT=production
DEBUG=false
```

## Security Considerations

1. Never commit sensitive environment variables to your repository
2. Use Railway's built-in secret management
3. Regularly rotate API keys and access credentials
4. Enable HTTPS for all external communications

## Cost Optimization

1. Monitor your Railway usage in the dashboard
2. Consider using Railway's free tier for development
3. Scale services based on actual usage patterns

## Next Steps

After successful deployment:

1. Update your frontend configuration to point to the new backend URL
2. Test all API endpoints
3. Set up monitoring and alerting
4. Configure CI/CD for automatic deployments
