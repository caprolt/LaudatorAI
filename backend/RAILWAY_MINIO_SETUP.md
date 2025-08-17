# MinIO Setup on Railway for LaudatorAI

This guide covers setting up MinIO file storage on Railway for the LaudatorAI application.

## Option 1: Railway MinIO Service (Recommended)

### Step 1: Add MinIO Service to Railway

1. In your Railway project dashboard, click "New Service"
2. Select "Deploy from Docker Image"
3. Use the MinIO Docker image: `minio/minio:latest`
4. Set the following environment variables:

```bash
MINIO_ROOT_USER=your-minio-user
MINIO_ROOT_PASSWORD=your-minio-password
```

5. Set the start command:
```bash
server /data --console-address ":9001"
```

### Step 2: Configure Backend Environment Variables

In your Railway backend service, add these environment variables:

```bash
# MinIO Configuration (internal Railway networking)
MINIO_ENDPOINT=your-minio-service.railway.internal:9000
MINIO_ACCESS_KEY=your-minio-user
MINIO_SECRET_KEY=your-minio-password
MINIO_BUCKET_NAME=laudatorai
MINIO_SECURE=false
```

### Step 3: Network Configuration

Railway automatically handles internal networking between services. The MinIO service will be accessible to your backend via the internal hostname.

## Option 2: External S3-Compatible Storage

### AWS S3 Example

```bash
MINIO_ENDPOINT=s3.amazonaws.com
MINIO_ACCESS_KEY=your-aws-access-key-id
MINIO_SECRET_KEY=your-aws-secret-access-key
MINIO_BUCKET_NAME=laudatorai
MINIO_SECURE=true
```

### Other S3-Compatible Services

- **DigitalOcean Spaces**: `nyc3.digitaloceanspaces.com`
- **Cloudflare R2**: `your-account-id.r2.cloudflarestorage.com`
- **Backblaze B2**: `s3.us-west-002.backblazeb2.com`

## Option 3: Railway's Built-in Storage

Railway offers storage solutions that can be used as S3-compatible alternatives:

1. Check Railway's marketplace for storage plugins
2. Configure as S3-compatible storage
3. Use the provided credentials

## Testing MinIO Connection

After deployment, test your MinIO connection:

1. Check the health endpoint: `https://your-app.railway.app/health`
2. Test file upload via the API: `POST /api/v1/resumes/upload`
3. Monitor logs in Railway dashboard

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Verify internal hostname is correct
   - Check that MinIO service is running
   - Ensure proper Railway networking

2. **Authentication Errors**
   - Verify access key and secret key
   - Check bucket permissions
   - Ensure bucket exists

3. **CORS Issues**
   - Configure MinIO CORS for your frontend domain
   - Update `BACKEND_CORS_ORIGINS`

### MinIO Console Access

To access MinIO console for management:

1. Go to your MinIO service in Railway
2. Access the console port (9001) via Railway's port forwarding
3. Login with your root credentials

## Security Considerations

1. **Use strong passwords** for MinIO root user
2. **Enable HTTPS** for external access
3. **Set up bucket policies** for proper access control
4. **Regular backups** of your data
5. **Monitor access logs**

## Cost Optimization

1. **MinIO on Railway**: Pay for compute resources
2. **External S3**: Pay for storage and bandwidth
3. **Monitor usage** in Railway dashboard
4. **Consider data lifecycle policies** for cost management

## Migration from Local Development

If migrating from local Docker setup:

1. Update environment variables
2. Test file upload/download functionality
3. Migrate existing files if needed
4. Update frontend configuration

## Next Steps

After successful MinIO setup:

1. Test all file operations (upload, download, delete)
2. Configure backup strategies
3. Set up monitoring and alerting
4. Document the setup for your team
