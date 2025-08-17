# Vercel Deployment Guide for LaudatorAI Frontend

This guide will help you deploy the LaudatorAI frontend to Vercel.

## Prerequisites

1. A Vercel account (https://vercel.com)
2. GitHub repository with your code
3. Vercel CLI (optional but recommended)

## Step 1: Connect Your Repository

1. Go to Vercel Dashboard
2. Click "New Project"
3. Import your GitHub repository
4. Select the `frontend` directory as the root directory
5. Vercel will automatically detect it as a Next.js project

## Step 2: Configure Environment Variables

In your Vercel project dashboard, go to "Settings" → "Environment Variables" and add:

### Required Variables

```bash
# Backend API URL (update with your Railway backend URL)
NEXT_PUBLIC_API_URL=https://your-backend.railway.app

# Environment
NEXT_PUBLIC_ENVIRONMENT=production
```

### Optional Variables

```bash
# Analytics (if using)
NEXT_PUBLIC_GA_ID=your-google-analytics-id
NEXT_PUBLIC_SENTRY_DSN=your-sentry-dsn
```

## Step 3: Configure Build Settings

Vercel should automatically detect the correct settings, but verify:

- **Framework Preset**: Next.js
- **Build Command**: `npm run build`
- **Output Directory**: `.next`
- **Install Command**: `npm install`

## Step 4: Deploy

1. Vercel will automatically deploy when you push to your main branch
2. Monitor the deployment in the Vercel dashboard
3. Check the deployment URL provided by Vercel

## Step 5: Configure Custom Domain (Optional)

1. In your Vercel project, go to "Settings" → "Domains"
2. Add your custom domain
3. Configure DNS settings as instructed by Vercel

## Step 6: Update Backend CORS

After getting your Vercel domain, update your Railway backend's CORS configuration:

```bash
# In Railway environment variables
BACKEND_CORS_ORIGINS=https://your-frontend-domain.vercel.app
```

## Environment-Specific Deployments

### Production

1. Deploy from the `main` branch
2. Set `NEXT_PUBLIC_ENVIRONMENT=production`
3. Use production backend URL

### Preview Deployments

1. Vercel automatically creates preview deployments for pull requests
2. Use staging backend URL for preview deployments
3. Set `NEXT_PUBLIC_ENVIRONMENT=staging`

## Configuration Files

### vercel.json

The project includes a `vercel.json` configuration file with:

- Build and deployment settings
- Security headers
- Function timeout configurations
- Environment variable references

### next.config.js

Ensure your `next.config.js` is optimized for production:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  experimental: {
    appDir: true,
  },
  images: {
    domains: ['your-backend-domain.railway.app'],
  },
}

module.exports = nextConfig
```

## Performance Optimization

### Build Optimization

1. **Code Splitting**: Next.js automatically handles code splitting
2. **Image Optimization**: Use Next.js Image component
3. **Bundle Analysis**: Run `npm run build` locally to analyze bundle size

### Runtime Optimization

1. **Caching**: Vercel provides automatic caching
2. **CDN**: Vercel's global CDN ensures fast loading
3. **Edge Functions**: Consider using Edge Functions for API routes

## Monitoring and Analytics

### Vercel Analytics

1. Enable Vercel Analytics in your project settings
2. Monitor Core Web Vitals
3. Track user interactions

### Error Tracking

1. Set up Sentry for error tracking
2. Configure error boundaries in your React components
3. Monitor API errors

## Security Considerations

### Environment Variables

1. Never expose sensitive data in client-side code
2. Use `NEXT_PUBLIC_` prefix only for public variables
3. Keep API keys and secrets server-side

### Security Headers

The `vercel.json` includes security headers:

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check build logs in Vercel dashboard
   - Verify all dependencies are in `package.json`
   - Ensure TypeScript compilation passes

2. **API Connection Issues**
   - Verify `NEXT_PUBLIC_API_URL` is correct
   - Check CORS configuration on backend
   - Test API endpoints directly

3. **Environment Variable Issues**
   - Ensure variables are set for the correct environment
   - Check variable names match your code
   - Redeploy after changing environment variables

### Debugging

1. **Local Testing**: Test locally with `npm run dev`
2. **Build Testing**: Test build locally with `npm run build`
3. **Vercel CLI**: Use `vercel dev` for local Vercel environment

## Cost Optimization

1. **Free Tier**: Vercel provides generous free tier
2. **Bandwidth**: Monitor bandwidth usage
3. **Function Execution**: Monitor serverless function usage

## Next Steps

After successful deployment:

1. Test all frontend functionality
2. Verify API integration with backend
3. Set up monitoring and alerting
4. Configure custom domain and SSL
5. Set up CI/CD for automatic deployments

## Advanced Configuration

### Edge Functions

For better performance, consider using Edge Functions:

```javascript
// app/api/health/route.ts
export const runtime = 'edge'

export async function GET() {
  return Response.json({ status: 'ok' })
}
```

### ISR (Incremental Static Regeneration)

For dynamic content that doesn't change frequently:

```javascript
// app/jobs/[id]/page.tsx
export async function generateStaticParams() {
  // Generate static pages for known job IDs
}

export const revalidate = 3600 // Revalidate every hour
```

### API Routes

If you need server-side API routes:

```javascript
// app/api/jobs/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  // Handle API requests
  return NextResponse.json({ jobs: [] })
}
```
