# LaudatorAI Deployment Guide

This guide covers deploying the LaudatorAI application with the backend on Railway and frontend on Vercel.

## Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Vercel        │    │   Railway       │    │   External      │
│   Frontend      │◄──►│   Backend       │◄──►│   Services      │
│   (Next.js)     │    │   (FastAPI)     │    │   (S3, Redis)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Prerequisites

1. **GitHub Repository**: Your code should be in a GitHub repository
2. **Railway Account**: Sign up at https://railway.app
3. **Vercel Account**: Sign up at https://vercel.com
4. **External Services**: 
   - S3-compatible storage (AWS S3, MinIO, etc.)
   - OpenAI API key (for AI features)

## Step 1: Deploy Backend to Railway

### 1.1 Create Railway Project

1. Go to Railway Dashboard
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Select the `backend` directory as the source

### 1.2 Add Required Services

#### PostgreSQL Database
1. In your Railway project, click "New Service"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically provide `DATABASE_URL`

#### Redis (for Celery)
1. Click "New Service"
2. Select "Database" → "Redis"
3. Railway will automatically provide `REDIS_URL`

### 1.3 Configure Environment Variables

In your Railway project dashboard, go to "Variables" tab:

```bash
# Database (auto-provided by Railway)
DATABASE_URL=postgresql://...

# Redis (auto-provided by Railway)
REDIS_URL=redis://...

# CORS Origins (update with your Vercel domain)
BACKEND_CORS_ORIGINS=https://your-frontend.vercel.app

# File Storage (S3/MinIO)
MINIO_ENDPOINT=your-s3-endpoint
MINIO_ACCESS_KEY=your-access-key
MINIO_SECRET_KEY=your-secret-key
MINIO_BUCKET_NAME=laudatorai
MINIO_SECURE=true

# AI Configuration
OPENAI_API_KEY=your-openai-api-key
LLM_PROVIDER=openai

# Environment
ENVIRONMENT=production
DEBUG=false
```

### 1.4 Deploy Backend

1. Railway will automatically deploy when you push to main branch
2. Monitor deployment logs
3. Test the health endpoint: `https://your-app.railway.app/health`

## Step 2: Deploy Frontend to Vercel

### 2.1 Create Vercel Project

1. Go to Vercel Dashboard
2. Click "New Project"
3. Import your GitHub repository
4. Select the `frontend` directory as root
5. Vercel will auto-detect Next.js

### 2.2 Configure Environment Variables

In Vercel project dashboard, go to "Settings" → "Environment Variables":

```bash
# Backend API URL (your Railway backend URL)
NEXT_PUBLIC_API_URL=https://your-backend.railway.app

# Environment
NEXT_PUBLIC_ENVIRONMENT=production
```

### 2.3 Deploy Frontend

1. Vercel will auto-deploy on push to main branch
2. Monitor deployment in dashboard
3. Get your deployment URL

## Step 3: Configure Integration

### 3.1 Update CORS Configuration

After getting your Vercel domain, update Railway backend CORS:

```bash
# In Railway environment variables
BACKEND_CORS_ORIGINS=https://your-frontend.vercel.app
```

### 3.2 Test Integration

1. Test frontend can connect to backend
2. Verify all API endpoints work
3. Test file upload/download functionality

## Step 4: Set Up Custom Domains (Optional)

### 4.1 Backend Domain (Railway)

1. In Railway project, go to "Settings" → "Domains"
2. Add custom domain
3. Configure DNS as instructed

### 4.2 Frontend Domain (Vercel)

1. In Vercel project, go to "Settings" → "Domains"
2. Add custom domain
3. Configure DNS settings

## Step 5: Set Up Background Workers (Optional)

For Celery background tasks:

1. Create separate Railway service for worker
2. Use same codebase but different start command
3. Set start command: `python scripts/start_celery_worker.py`

## Environment Configurations

### Development
```bash
# Backend (Railway)
ENVIRONMENT=development
DEBUG=true

# Frontend (Vercel)
NEXT_PUBLIC_ENVIRONMENT=development
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Staging
```bash
# Backend (Railway)
ENVIRONMENT=staging
DEBUG=false

# Frontend (Vercel)
NEXT_PUBLIC_ENVIRONMENT=staging
NEXT_PUBLIC_API_URL=https://staging-backend.railway.app
```

### Production
```bash
# Backend (Railway)
ENVIRONMENT=production
DEBUG=false

# Frontend (Vercel)
NEXT_PUBLIC_ENVIRONMENT=production
NEXT_PUBLIC_API_URL=https://production-backend.railway.app
```

## Monitoring and Maintenance

### Railway Backend Monitoring

1. **Logs**: View in Railway dashboard
2. **Health Checks**: Monitor `/health` endpoint
3. **Database**: Monitor PostgreSQL usage
4. **Redis**: Monitor Redis usage

### Vercel Frontend Monitoring

1. **Analytics**: Enable Vercel Analytics
2. **Performance**: Monitor Core Web Vitals
3. **Errors**: Set up error tracking (Sentry)
4. **Uptime**: Monitor deployment status

### External Services

1. **S3/MinIO**: Monitor storage usage
2. **OpenAI**: Monitor API usage and costs
3. **Custom Domains**: Monitor SSL certificates

## Troubleshooting

### Common Issues

#### Backend Issues
1. **Database Connection**: Check `DATABASE_URL` in Railway
2. **Redis Connection**: Verify `REDIS_URL` is set
3. **CORS Errors**: Update `BACKEND_CORS_ORIGINS`
4. **File Upload**: Verify S3/MinIO configuration

#### Frontend Issues
1. **API Connection**: Check `NEXT_PUBLIC_API_URL`
2. **Build Failures**: Check build logs in Vercel
3. **Environment Variables**: Verify variable names

#### Integration Issues
1. **CORS**: Ensure frontend domain is in backend CORS list
2. **HTTPS**: Use HTTPS URLs in production
3. **Timeouts**: Check API response times

### Debugging Steps

1. **Local Testing**: Test locally first
2. **Logs**: Check Railway and Vercel logs
3. **Health Checks**: Test `/health` endpoint
4. **Network**: Use browser dev tools to debug API calls

## Security Considerations

### Environment Variables
- Never commit secrets to repository
- Use Railway and Vercel secret management
- Rotate API keys regularly

### CORS Configuration
- Only allow necessary origins
- Use HTTPS in production
- Validate CORS headers

### API Security
- Implement rate limiting
- Validate all inputs
- Use HTTPS for all communications

## Cost Optimization

### Railway
- Monitor usage in dashboard
- Use free tier for development
- Scale based on actual usage

### Vercel
- Free tier is generous
- Monitor bandwidth usage
- Optimize bundle size

### External Services
- Monitor S3 storage costs
- Track OpenAI API usage
- Use appropriate service tiers

## CI/CD Setup

### Automatic Deployments

1. **Railway**: Auto-deploys on push to main branch
2. **Vercel**: Auto-deploys on push to main branch
3. **Preview Deployments**: Vercel creates previews for PRs

### Manual Deployments

```bash
# Railway CLI
railway login
railway link
railway up

# Vercel CLI
vercel login
vercel --prod
```

## Backup and Recovery

### Database Backups
- Railway provides automatic PostgreSQL backups
- Consider additional backup strategies
- Test restore procedures

### File Storage
- S3/MinIO provides redundancy
- Implement backup strategies for critical files
- Test file recovery procedures

## Performance Optimization

### Backend (Railway)
- Optimize database queries
- Use connection pooling
- Implement caching strategies

### Frontend (Vercel)
- Optimize bundle size
- Use Next.js Image optimization
- Implement proper caching

## Next Steps

After successful deployment:

1. **Testing**: Comprehensive testing of all features
2. **Monitoring**: Set up monitoring and alerting
3. **Documentation**: Update documentation with production URLs
4. **Security**: Security audit and penetration testing
5. **Performance**: Performance testing and optimization
6. **Backup**: Implement backup and recovery procedures

## Support Resources

- **Railway Documentation**: https://docs.railway.app
- **Vercel Documentation**: https://vercel.com/docs
- **Next.js Documentation**: https://nextjs.org/docs
- **FastAPI Documentation**: https://fastapi.tiangolo.com
