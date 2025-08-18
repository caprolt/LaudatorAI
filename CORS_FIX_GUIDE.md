# CORS Fix Guide for LaudatorAI

## Problem
Your frontend deployed on Vercel (`https://laudator-ai.vercel.app`) is getting CORS errors when trying to communicate with your backend deployed on Railway (`https://laudatorai-production.up.railway.app`).

## Root Cause
The Railway backend doesn't have the correct CORS origins configured to allow requests from your Vercel frontend.

## Solution

### 1. Update Railway Environment Variables

You need to add the `BACKEND_CORS_ORIGINS` environment variable to your Railway backend deployment:

1. Go to your Railway dashboard
2. Navigate to your backend service
3. Go to the "Variables" tab
4. Add a new environment variable:

**Variable Name:** `BACKEND_CORS_ORIGINS`
**Value:** `["https://laudator-ai.vercel.app","https://laudator-ai-git-main-caprolt.vercel.app","https://laudator-ai-caprolt.vercel.app"]`

### 2. Alternative: Use Railway CLI

If you prefer using the Railway CLI:

```bash
railway variables set BACKEND_CORS_ORIGINS='["https://laudator-ai.vercel.app","https://laudator-ai-git-main-caprolt.vercel.app","https://laudator-ai-caprolt.vercel.app"]'
```

### 3. Redeploy the Backend

After setting the environment variable, redeploy your backend:

1. In Railway dashboard, go to "Deployments"
2. Click "Deploy" to trigger a new deployment
3. Or push a new commit to your main branch to trigger automatic deployment

### 4. Verify the Fix

After deployment, test the connection:

1. Open your frontend at `https://laudator-ai.vercel.app`
2. Try uploading a resume or making any API call
3. Check the browser console - CORS errors should be gone

## Code Changes Made

### Backend Changes

1. **Updated `backend/app/main.py`**:
   - Modified CORS fallback to include your Vercel frontend URLs
   - Added proper logging for CORS configuration

2. **Updated `backend/.env.example`**:
   - Added production frontend URL to CORS origins

3. **Created `backend/.env.production.example`**:
   - Production-specific environment template

### Frontend Changes

1. **Created `frontend/public/` directory**:
   - Added favicon files to prevent 404 errors

2. **Updated `frontend/src/app/layout.tsx`**:
   - Added proper favicon metadata

## Environment Variables Reference

### Development
```bash
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]
```

### Production
```bash
BACKEND_CORS_ORIGINS=["https://laudator-ai.vercel.app","https://laudator-ai-git-main-caprolt.vercel.app","https://laudator-ai-caprolt.vercel.app"]
```

## Troubleshooting

### If CORS errors persist:

1. **Check Railway logs**:
   - Go to Railway dashboard → your service → "Deployments" → latest deployment → "Logs"
   - Look for CORS-related messages

2. **Verify environment variable**:
   - In Railway dashboard → "Variables" tab
   - Ensure `BACKEND_CORS_ORIGINS` is set correctly

3. **Test with curl**:
   ```bash
   curl -H "Origin: https://laudator-ai.vercel.app" \
        -H "Access-Control-Request-Method: POST" \
        -H "Access-Control-Request-Headers: Content-Type" \
        -X OPTIONS \
        https://laudatorai-production.up.railway.app/api/v1/resumes/upload
   ```

4. **Check browser network tab**:
   - Open browser dev tools → Network tab
   - Look for preflight OPTIONS requests
   - Check if they return proper CORS headers

### If you need to allow all origins (not recommended for production):

```bash
BACKEND_CORS_ORIGINS=["*"]
```

## Security Notes

- Only include the specific frontend URLs you need
- Avoid using `["*"]` in production
- Consider using environment-specific CORS configurations
- Monitor your Railway logs for any CORS-related issues

## Next Steps

1. Set the environment variable in Railway
2. Redeploy the backend
3. Test the frontend-backend communication
4. Monitor logs for any issues
5. Consider setting up proper monitoring for CORS errors
