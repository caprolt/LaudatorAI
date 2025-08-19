# Railway Deployment Guide

## Why AWS S3 Instead of MinIO for Railway?

### MinIO Issues with Railway
- ❌ **No managed MinIO service** on Railway
- ❌ **Additional costs** for running MinIO as a separate service
- ❌ **Complex configuration** and maintenance
- ❌ **Not scalable** for production workloads

### AWS S3 Benefits for Railway
- ✅ **Industry standard** for file storage
- ✅ **Excellent integration** with Railway
- ✅ **Cost-effective** for small to medium usage
- ✅ **Built-in CDN** capabilities
- ✅ **Automatic scaling** and reliability
- ✅ **Your code already supports S3** (via boto3)

## Quick Setup for Railway

### 1. Create AWS S3 Bucket

1. Go to [AWS S3 Console](https://console.aws.amazon.com/s3/)
2. Create a new bucket named `laudatorai-files` (or your preferred name)
3. Choose a region (e.g., `us-east-1`)
4. Configure bucket settings:
   - **Block Public Access**: Keep all blocks enabled (default)
   - **Versioning**: Disabled (for cost savings)
   - **Encryption**: Server-side encryption with Amazon S3 managed keys

### 2. Create AWS IAM User

1. Go to [AWS IAM Console](https://console.aws.amazon.com/iam/)
2. Create a new user with programmatic access
3. Attach the `AmazonS3FullAccess` policy (or create a custom policy for better security)
4. Save the Access Key ID and Secret Access Key

### 3. Deploy to Railway

1. **Connect your GitHub repository** to Railway
2. **Add PostgreSQL service** to your Railway project
3. **Add Redis service** to your Railway project
4. **Configure environment variables** in Railway:

```bash
# Required
BACKEND_CORS_ORIGINS=https://your-frontend-domain.vercel.app,http://localhost:3000
ENVIRONMENT=production
DEBUG=false

# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
AWS_REGION=us-east-1
S3_BUCKET_NAME=laudatorai-files

# Optional
OPENAI_API_KEY=your-openai-api-key-here
```

### 4. Deploy and Test

1. Railway will automatically deploy your backend
2. Test the resume upload functionality
3. Check the logs for any issues

## Alternative: Cloudflare R2 (Cheaper Option)

If you want to save costs, consider Cloudflare R2:

### 1. Create R2 Bucket

1. Go to [Cloudflare R2 Console](https://dash.cloudflare.com/)
2. Create a new R2 bucket named `laudatorai-files`
3. Note your Account ID

### 2. Create API Token

1. Go to [Cloudflare API Tokens](https://dash.cloudflare.com/profile/api-tokens)
2. Create a custom token with R2 permissions
3. Save the Access Key ID and Secret Access Key

### 3. Configure Railway Environment

```bash
# Cloudflare R2 Configuration
AWS_ACCESS_KEY_ID=your-r2-access-key-id
AWS_SECRET_ACCESS_KEY=your-r2-secret-access-key
AWS_REGION=auto
S3_BUCKET_NAME=laudatorai-files
S3_ENDPOINT_URL=https://your-account-id.r2.cloudflarestorage.com
```

## Cost Comparison

| Service | Storage | Transfer | CDN | Monthly Cost (1GB) |
|---------|---------|----------|-----|-------------------|
| AWS S3 | $0.023/GB | $0.09/GB | $0.085/GB | ~$0.20 |
| Cloudflare R2 | $0.015/GB | Free | Free | ~$0.015 |
| MinIO on Railway | $0.50/GB | $0.10/GB | N/A | ~$0.60 |

## Security Best Practices

### AWS S3 Security
1. **Use IAM roles** instead of access keys when possible
2. **Enable bucket versioning** for critical data
3. **Set up bucket policies** to restrict access
4. **Enable server-side encryption**
5. **Use presigned URLs** for secure file access

### Environment Variables Security
1. **Never commit secrets** to your repository
2. **Use Railway's secret management**
3. **Rotate access keys** regularly
4. **Monitor access logs**

## Troubleshooting

### Common Issues

1. **"Access Denied" errors**:
   - Check IAM permissions
   - Verify bucket name and region
   - Ensure access keys are correct

2. **"Bucket not found" errors**:
   - Verify bucket exists in the correct region
   - Check bucket name spelling

3. **CORS errors**:
   - Configure CORS on your S3 bucket
   - Update `BACKEND_CORS_ORIGINS` in Railway

### S3 Bucket CORS Configuration

Add this CORS configuration to your S3 bucket:

```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
        "AllowedOrigins": ["https://your-frontend-domain.vercel.app"],
        "ExposeHeaders": ["ETag"]
    }
]
```

## Migration from MinIO

If you're currently using MinIO locally and want to migrate to S3:

1. **Update your local `.env`** to use S3 for testing
2. **Test file uploads** locally with S3
3. **Deploy to Railway** with S3 configuration
4. **Migrate existing files** (if any) from MinIO to S3

## Monitoring and Logs

### Railway Logs
- Check Railway dashboard for deployment logs
- Monitor application logs for errors
- Set up alerts for failed deployments

### S3 Monitoring
- Enable S3 access logging
- Monitor bucket usage and costs
- Set up CloudWatch alarms for unusual activity

## Next Steps

1. **Deploy your backend** to Railway with S3
2. **Test resume uploads** thoroughly
3. **Deploy your frontend** to Vercel
4. **Configure CORS** between frontend and backend
5. **Set up monitoring** and alerts
6. **Optimize costs** based on usage patterns

## Support

If you encounter issues:
1. Check Railway logs first
2. Verify environment variables
3. Test S3 connectivity
4. Review this guide for common solutions
5. Check the main [README.md](../README.md) for additional help
