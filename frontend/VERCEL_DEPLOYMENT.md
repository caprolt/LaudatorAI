# Vercel Deployment Guide

## Environment Variables

Make sure to set the following environment variables in your Vercel project settings:

### Required Environment Variables

1. **NEXT_PUBLIC_API_URL** (Required)
   - **Production**: `https://laudatorai-production.up.railway.app`
   - **Development**: `http://localhost:8000/api/v1`
   - **Description**: The base URL for the backend API

2. **NEXT_PUBLIC_ENVIRONMENT** (Optional)
   - **Production**: `production`
   - **Development**: `development`
   - **Description**: Environment identifier for logging and debugging

### Setting Environment Variables in Vercel

1. Go to your Vercel dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add the following variables:

```
NEXT_PUBLIC_API_URL=https://laudatorai-production.up.railway.app
NEXT_PUBLIC_ENVIRONMENT=production
```

### Important Notes

- **Never commit `.env.local` files** - they should be gitignored
- **Always use HTTPS in production** - the config will automatically convert HTTP to HTTPS in production
- **Environment variables must be prefixed with `NEXT_PUBLIC_`** to be accessible in the browser

## Deployment Steps

1. **Set Environment Variables**: Configure the environment variables in Vercel dashboard
2. **Deploy**: Push to your main branch or create a new deployment
3. **Verify**: Check that the API calls are working correctly

## Troubleshooting

### Mixed Content Errors
If you see "Mixed Content" errors in the browser console:
1. Check that `NEXT_PUBLIC_API_URL` is set to use HTTPS in production
2. Verify that the backend is accessible via HTTPS
3. Check browser console for the logged API URLs

### API Connection Issues
1. Verify the backend is running and accessible
2. Check CORS configuration on the backend
3. Ensure environment variables are set correctly in Vercel

## Local Development

For local development, create a `.env.local` file (this will be gitignored):

```bash
# API Configuration for local development
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_ENVIRONMENT=development
```

## Build and Deploy

```bash
# Install dependencies
npm install

# Build for production
npm run build

# Deploy to Vercel
vercel --prod
```

## Monitoring

- Check Vercel deployment logs for build errors
- Monitor browser console for API errors
- Use Vercel Analytics to track performance
