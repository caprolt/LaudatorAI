# CORS Fix Guide for LaudatorAI

## Problem
Your frontend at `https://laudator-ai.vercel.app` is getting CORS errors when trying to communicate with your backend at `https://laudatorai-production.up.railway.app`. The error message is:

```
Access to fetch at 'https://laudatorai-production.up.railway.app/api/v1/jobs/extract' from origin 'https://laudator-ai.vercel.app' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

## Root Cause
Two environment variables are missing in your Railway deployment:

1. **`BACKEND_CORS_ORIGINS`**: This variable tells the backend which frontend domains are allowed to make requests
2. **`PORT`**: This variable sets the port on which the backend server runs (Railway requires this to be explicitly set to `8000`)

## Solution

### Step 1: Go to Railway Dashboard
1. Navigate to your Railway project: https://railway.app/dashboard
2. Select your backend service (the one deployed at `laudatorai-production.up.railway.app`)

### Step 2: Add Environment Variables
1. Go to the **Variables** tab in your backend service
2. Click **"New Variable"** for each of the following:

#### Required Environment Variables:

**Variable 1:**
   - **Variable name**: `BACKEND_CORS_ORIGINS`
   - **Variable value**: `https://laudator-ai.vercel.app,https://laudator-ai-tannercline-5407s-projects.vercel.app,https://laudator-ai-git-main-tannercline-5407s-projects.vercel.app,http://localhost:3000,http://localhost:3001`

**Variable 2:**
   - **Variable name**: `PORT`
   - **Variable value**: `8000`

### Step 3: Save and Deploy
1. Click **"Save"** to add the variable
2. Railway will automatically redeploy your service
3. Wait for the deployment to complete (usually 1-2 minutes)

### Step 4: Test the Fix
1. Go to your frontend: https://laudator-ai.vercel.app
2. Try submitting a job description
3. Check the browser console - you should no longer see CORS errors

### Step 5: Verify in Logs
1. In Railway dashboard, go to your backend service
2. Check the **Logs** tab
3. Look for a message like: `CORS origins: ['https://laudator-ai.vercel.app', ...]`

## What This Does

### BACKEND_CORS_ORIGINS
The `BACKEND_CORS_ORIGINS` environment variable tells your FastAPI backend which domains are allowed to make cross-origin requests. By setting it to include your Vercel frontend domains, the backend will add the necessary CORS headers to allow the frontend to communicate with it.

### PORT
The `PORT` environment variable is required by Railway to specify which port your application should listen on. Setting it to `8000` ensures your FastAPI backend runs on the correct port that Railway expects.

## Alternative: Quick Fix Script
If you want to test this locally first, you can run:
```bash
cd backend
python set_cors_env.py
```

This will show you the exact environment variable value and test the CORS configuration.

## Troubleshooting
- If you still see CORS errors after setting the variables, wait a few minutes for the deployment to complete
- Make sure you're using the exact variable names: `BACKEND_CORS_ORIGINS` and `PORT` (case sensitive)
- Check Railway logs for any deployment errors
- Verify the frontend URL in the `BACKEND_CORS_ORIGINS` variable matches your actual Vercel deployment URL
- Ensure the `PORT` variable is set to exactly `8000` (no quotes needed)
- If the backend still won't start, check Railway logs for port binding errors

## Expected Result
After setting this environment variable, your frontend should be able to successfully make API calls to your backend without any CORS errors.
