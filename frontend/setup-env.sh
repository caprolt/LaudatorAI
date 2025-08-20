#!/bin/bash

# Environment Setup Script for LaudatorAI Frontend

echo "Setting up environment for LaudatorAI Frontend..."

# Check if .env.local already exists
if [ -f ".env.local" ]; then
    echo "Warning: .env.local already exists. Backing up to .env.local.backup"
    mv .env.local .env.local.backup
fi

# Create .env.local for local development
cat > .env.local << EOF
# API Configuration for local development
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_ENVIRONMENT=development

# Optional: Analytics and Monitoring
# NEXT_PUBLIC_SENTRY_DSN=your_sentry_dsn_here
# NEXT_PUBLIC_GA_ID=your_google_analytics_id_here
EOF

echo "✅ Created .env.local for local development"
echo ""
echo "📝 Environment Variables:"
echo "   NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1"
echo "   NEXT_PUBLIC_ENVIRONMENT=development"
echo ""
echo "🚀 For production deployment on Vercel, set these environment variables:"
echo "   NEXT_PUBLIC_API_URL=https://laudatorai-production.up.railway.app"
echo "   NEXT_PUBLIC_ENVIRONMENT=production"
echo ""
echo "📖 See VERCEL_DEPLOYMENT.md for detailed deployment instructions"
