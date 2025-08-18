# Railway Deployment Guide for LaudatorAI Backend

This guide will help you deploy the LaudatorAI backend to Railway successfully.

## Prerequisites

1. A Railway account (https://railway.app)
2. GitHub repository with your code
3. Railway CLI (optional but recommended)

## Step 1: Create Railway Project

1. Go to Railway Dashboard
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Select the `backend` directory as the source

## Step 2: Add Required Services

### PostgreSQL Database
1. In your Railway project, click "New Service"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically provide the `DATABASE_URL` environment variable

### Redis Service
1. Click "New Service" again
2. Select "Database" → "Redis"
3. Railway will automatically provide the `REDIS_URL` environment variable

## Step 3: Configure Environment Variables

In your backend service, go to "Variables" tab and add:

### Required Variables (Auto-provided by Railway)
```bash
# These are automatically set by Railway when you add the services
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
PORT=8000
```

### Required Variables (Manual setup)
```bash
# CORS Configuration - Add your frontend domain
BACKEND_CORS_ORIGINS=https://your-frontend-domain.vercel.app,http://localhost:3000

# Environment
ENVIRONMENT=production
DEBUG=false

# Optional: OpenAI API Key (if using OpenAI)
OPENAI_API_KEY=your-openai-api-key
```

### Optional Variables
```bash
# Sentry for error tracking
SENTRY_DSN=your-sentry-dsn

# MinIO/S3 configuration (if using external storage)
MINIO_ENDPOINT=your-minio-endpoint
MINIO_ACCESS_KEY=your-minio-access-key
MINIO_SECRET_KEY=your-minio-secret-key
MINIO_BUCKET_NAME=laudatorai
MINIO_SECURE=true
```

## Step 4: Configure Service Dependencies

1. In your backend service settings
2. Go to "Settings" → "Dependencies"
3. Add dependencies on:
   - PostgreSQL service
   - Redis service

## Step 5: Deploy

1. Railway will automatically deploy when you push to your main branch
2. Monitor the deployment in the Railway dashboard
3. Check the deployment logs for any errors

## Step 6: Verify Deployment

### Test Health Endpoint
```bash
curl https://your-backend.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "LaudatorAI API",
  "timestamp": 1234567890,
  "version": "0.1.0",
  "environment": "production"
}
```

### Test API Documentation
Visit: `https://your-backend.railway.app/docs`

## Step 7: Update Frontend Configuration

In your Vercel frontend, update the environment variable:
```bash
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

## Troubleshooting

### Common Issues

#### 1. 502 Bad Gateway
- Check Railway logs for startup errors
- Verify all environment variables are set
- Ensure PostgreSQL and Redis services are running

#### 2. CORS Errors
- Update `BACKEND_CORS_ORIGINS` with your frontend domain
- Include both production and development URLs

#### 3. Database Connection Issues
- Verify `DATABASE_URL` is correct
- Check if PostgreSQL service is healthy
- Ensure database migrations run successfully

#### 4. Redis Connection Issues
- Verify `REDIS_URL` is correct
- Check if Redis service is healthy

### Debugging Steps

#### Check Railway Logs
1. Go to your backend service
2. Click "Deployments" tab
3. Click on the latest deployment
4. Check the logs for error messages

#### Test Locally with Railway Environment
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Link to your project
railway link

# Test locally with Railway environment
railway run python start.py
```

#### Verify Environment Variables
```bash
# View Railway environment variables
railway variables

# Test specific variable
railway run echo $DATABASE_URL
```

## Monitoring

### Health Checks
Railway automatically monitors the `/health` endpoint. If it fails:
- Check application logs
- Verify all services are running
- Test the health endpoint manually

### Resource Usage
Monitor your service's resource usage:
- CPU usage
- Memory usage
- Disk space

### Logs
Railway provides real-time logs:
- Application logs
- Build logs
- Deployment logs

## Cost Optimization

### Free Tier Limits
- 500 hours per month
- 1GB RAM per service
- Shared CPU resources

### Upgrading
If you need more resources:
1. Go to your service settings
2. Click "Upgrade"
3. Choose a plan that fits your needs

## Security Best Practices

### Environment Variables
- Never commit secrets to your repository
- Use Railway's secret management
- Rotate API keys regularly

### CORS Configuration
- Only allow necessary origins
- Don't use wildcards in production
- Include both HTTP and HTTPS if needed

### Database Security
- Use strong passwords
- Enable SSL connections
- Regular backups

## Advanced Configuration

### Custom Domains
1. Go to your service settings
2. Click "Domains"
3. Add your custom domain
4. Configure DNS settings

### SSL Certificates
Railway automatically provides SSL certificates for:
- Railway subdomains
- Custom domains

### Environment-Specific Deployments
You can create multiple environments:
- Development
- Staging
- Production

## Support

If you encounter issues:
1. Check this troubleshooting guide
2. Review Railway documentation
3. Check application logs
4. Contact Railway support

## Next Steps

After successful deployment:
1. Test all API endpoints
2. Verify frontend integration
3. Set up monitoring and alerts
4. Configure custom domain (optional)
5. Set up CI/CD for automatic deployments
