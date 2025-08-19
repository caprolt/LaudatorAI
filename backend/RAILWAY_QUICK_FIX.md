# Railway Deployment Quick Fix Guide

## Issues Identified from Debug Output

Based on your `railway run python debug_railway.py` output, here are the main issues:

### ❌ Critical Issues
1. **Missing DATABASE_URL** - PostgreSQL service not added to Railway project
2. **Missing REDIS_URL** - Redis service not added to Railway project  
3. **Missing ENVIRONMENT** - Not set in Railway variables
4. **Missing PORT** - Not set in Railway variables
5. **Missing HOST** - Not set in Railway variables
6. **Redis Connection Failed** - DNS resolution error for `redis.railway.internal`

### ⚠️ Warnings
1. **WeasyPrint Dependencies** - Missing system libraries for PDF generation
2. **Optional Variables** - BACKEND_CORS_ORIGINS, OPENAI_API_KEY, etc. not set

## Quick Fix Steps

### Step 1: Add Required Services to Railway Project

1. Go to your Railway project dashboard
2. Click **"New Service"** → **"Database"** → **"PostgreSQL"**
3. Click **"New Service"** → **"Database"** → **"Redis"**

These services will automatically provide:
- `DATABASE_URL` (PostgreSQL connection string)
- `REDIS_URL` (Redis connection string)

### Step 2: Set Environment Variables

In your Railway backend service, go to **"Variables"** tab and add:

```bash
# Required
BACKEND_CORS_ORIGINS=https://your-frontend-domain.vercel.app,http://localhost:3000
ENVIRONMENT=production
DEBUG=false

# Optional
OPENAI_API_KEY=your-openai-api-key
MINIO_ENDPOINT=your-minio-endpoint
MINIO_ACCESS_KEY=your-minio-access-key
MINIO_SECRET_KEY=your-minio-secret-key
```

### Step 3: Configure Service Dependencies

1. Go to your backend service → **"Settings"** → **"Dependencies"**
2. Add dependencies on:
   - PostgreSQL service
   - Redis service

### Step 4: Redeploy

1. Push your code to trigger a new deployment, OR
2. Manually trigger a redeploy from the Railway dashboard

### Step 5: Verify Deployment

1. Check Railway logs for any errors
2. Test health endpoint: `https://your-app.railway.app/health`
3. Test API docs: `https://your-app.railway.app/docs`
4. Run debug script: `railway run python debug_railway.py`

## Files Updated

The following files have been updated to fix the issues:

1. **`nixpacks.toml`** - Added WeasyPrint system dependencies
2. **`start.py`** - Added default environment variable handling
3. **`railway.env.template`** - Environment variables template
4. **`set_railway_env.py`** - Environment setup script
5. **`fix_railway_deployment_complete.py`** - Comprehensive fix script

## Expected Results After Fix

After following these steps, your debug output should show:

```
✓ DATABASE_URL: postgresql://...
✓ REDIS_URL: redis://...
✓ ENVIRONMENT: production
✓ PORT: 8000
✓ HOST: 0.0.0.0
✓ Redis connection successful
✓ Database connection successful
✓ FastAPI app created successfully
```

## Troubleshooting

If you still encounter issues:

1. **Check Railway Logs** - Look for specific error messages
2. **Verify Services** - Ensure PostgreSQL and Redis services are running
3. **Test Locally** - Run `railway run python debug_railway.py` to test with Railway environment
4. **Check Dependencies** - Ensure service dependencies are configured correctly

## Next Steps

After successful deployment:

1. Update your frontend to use the new backend URL
2. Test all API endpoints
3. Set up monitoring and alerts
4. Configure custom domain (optional)

## Support

If you need help:
1. Check the detailed documentation in `RAILWAY_DEPLOYMENT.md`
2. Review troubleshooting guide in `RAILWAY_TROUBLESHOOTING.md`
3. Run the comprehensive fix script: `python fix_railway_deployment_complete.py`
