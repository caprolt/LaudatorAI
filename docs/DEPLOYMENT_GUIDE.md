# LaudatorAI Deployment Guide

## 🚀 Cloud Deployment

This guide covers the deployment process for LaudatorAI using modern cloud platforms.

## 📋 Prerequisites

### Required Accounts
- GitHub account
- Railway account (for backend)
- Vercel account (for frontend)
- OpenAI API key

## 🏗️ Deployment Setup

### 1. Backend Deployment (Railway)

#### Step 1: Connect Repository to Railway
1. Go to [Railway](https://railway.app)
2. Create a new project
3. Connect your GitHub repository
4. Select the `backend` directory as the source

#### Step 2: Add Services
1. Add PostgreSQL service
2. Add Redis service
3. Configure environment variables

#### Step 3: Configure Environment Variables
Set the following environment variables in Railway:
- `POSTGRES_SERVER`: Your Railway PostgreSQL host
- `POSTGRES_USER`: Your Railway PostgreSQL user
- `POSTGRES_PASSWORD`: Your Railway PostgreSQL password
- `POSTGRES_DB`: Your Railway PostgreSQL database name
- `REDIS_URL`: Your Railway Redis URL
- `OPENAI_API_KEY`: Your OpenAI API key
- `MINIO_ENDPOINT`: Your MinIO endpoint (or use Railway's S3)
- `MINIO_ACCESS_KEY`: Your MinIO access key
- `MINIO_SECRET_KEY`: Your MinIO secret key
- `MINIO_BUCKET_NAME`: Your MinIO bucket name

### 2. Frontend Deployment (Vercel)

#### Step 1: Connect Repository to Vercel
1. Go to [Vercel](https://vercel.com)
2. Create a new project
3. Connect your GitHub repository
4. Select the `frontend` directory as the source

#### Step 2: Configure Environment Variables
Set the following environment variables in Vercel:
- `NEXT_PUBLIC_API_URL`: Your Railway backend URL (e.g., `https://your-app.railway.app`)

## 🔧 Configuration Details

### Environment Variables

#### Backend (Railway)
- `POSTGRES_SERVER`: Database host
- `POSTGRES_USER`: Database user
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_DB`: Database name
- `REDIS_URL`: Redis connection URL
- `OPENAI_API_KEY`: OpenAI API key
- `MINIO_ENDPOINT`: File storage endpoint
- `MINIO_ACCESS_KEY`: File storage access key
- `MINIO_SECRET_KEY`: File storage secret key
- `MINIO_BUCKET_NAME`: File storage bucket name

#### Frontend (Vercel)
- `NEXT_PUBLIC_API_URL`: Backend API URL

## 📊 Monitoring Setup

### Grafana Dashboard
1. Access Grafana at the configured URL
2. Login with admin/admin (or your custom password)
3. The LaudatorAI dashboard should be automatically provisioned
4. Key metrics to monitor:
   - API response times
   - Error rates
   - System resource usage
   - Database connections

## 📊 Monitoring & Health Checks

### Railway Monitoring
Railway provides built-in monitoring:
- Application logs
- Resource usage
- Health checks
- Automatic restarts

### Vercel Monitoring
Vercel provides:
- Performance analytics
- Error tracking
- Function logs
- Real-time metrics

### Health Checks
```bash
# Check backend health
curl -f https://your-app.railway.app/health

# Check frontend
curl -f https://your-app.vercel.app
```

## 🧪 Testing

### Load Testing
```bash
# Test backend API
curl -X POST https://your-app.railway.app/api/v1/jobs/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/job"}'

# Test frontend
curl -f https://your-app.vercel.app
```

## 🔄 Rollback Procedures

### Railway Rollback
1. Go to Railway dashboard
2. Navigate to your service
3. Click on "Deployments"
4. Select a previous deployment
5. Click "Redeploy"

### Vercel Rollback
1. Go to Vercel dashboard
2. Navigate to your project
3. Click on "Deployments"
4. Select a previous deployment
5. Click "Redeploy"

## 🚨 Troubleshooting

### Common Issues

#### 1. Railway Backend Issues
- Check Railway logs in the dashboard
- Verify environment variables
- Check service dependencies
- Review resource limits

#### 2. Vercel Frontend Issues
- Check Vercel deployment logs
- Verify environment variables
- Check build output
- Review function logs

#### 3. API Connection Issues
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check CORS configuration
- Test API endpoints directly
- Verify SSL certificates

### Log Analysis
- **Railway**: Use the Railway dashboard for backend logs
- **Vercel**: Use the Vercel dashboard for frontend logs
- **Real-time**: Both platforms provide real-time log streaming

## 🔒 Security Considerations

### Cloud Security Checklist
- [ ] Environment variables properly configured
- [ ] API keys secured
- [ ] CORS settings configured
- [ ] Database access restricted
- [ ] Regular dependency updates
- [ ] Monitoring alerts enabled

### Security Features
Both Railway and Vercel provide:
- Automatic SSL/TLS
- DDoS protection
- Global CDN
- Security headers
- Automatic updates

## 📈 Performance Optimization

### Railway Optimization
- Monitor resource usage
- Optimize Docker images
- Use connection pooling
- Implement caching strategies

### Vercel Optimization
- Enable edge caching
- Optimize bundle size
- Use image optimization
- Implement ISR (Incremental Static Regeneration)

### Database Optimization
- Regular VACUUM operations
- Proper indexing
- Connection pooling
- Query optimization

## 🔄 Maintenance

### Regular Maintenance Tasks
1. **Daily**
   - Check application health
   - Monitor error rates
   - Review logs for issues

2. **Weekly**
   - Database maintenance
   - Dependency updates
   - Security reviews

3. **Monthly**
   - Performance review
   - Backup verification
   - Cost optimization

### Backup Procedures
Railway provides automatic backups for PostgreSQL. For additional backups:
- Use Railway's built-in backup features
- Export data periodically
- Store backups in secure location

## 🎯 Launch Checklist

### Pre-Launch
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] CORS settings updated
- [ ] Monitoring enabled
- [ ] Domain configured (optional)
- [ ] SSL certificates valid

### Launch Day
- [ ] Deploy to Railway
- [ ] Deploy to Vercel
- [ ] Verify all services healthy
- [ ] Run smoke tests
- [ ] Monitor for issues
- [ ] Test API connectivity

### Post-Launch
- [ ] Monitor performance
- [ ] Gather user feedback
- [ ] Address any issues
- [ ] Plan future improvements

## 📞 Support

For deployment issues:
1. Check the troubleshooting section
2. Review Railway/Vercel logs
3. Verify environment variables
4. Test API endpoints directly

## 🔗 Useful Commands

```bash
# Check backend health
curl -f https://your-app.railway.app/health

# Test API endpoint
curl -X GET https://your-app.railway.app/api/v1/jobs/

# Check frontend
curl -f https://your-app.vercel.app

# View Railway logs
# Use Railway dashboard

# View Vercel logs
# Use Vercel dashboard
```

This deployment guide ensures a smooth and secure launch of LaudatorAI in both staging and production environments.
