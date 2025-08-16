#!/bin/bash

# LaudatorAI Production Deployment Script
set -e

echo "🚀 Starting LaudatorAI production deployment..."

# Check if .env.production exists
if [ ! -f .env.production ]; then
    echo "❌ .env.production file not found. Please copy .env.production.template and configure it."
    exit 1
fi

# Check if SSL certificates exist
if [ ! -f nginx/ssl/cert.pem ] || [ ! -f nginx/ssl/key.pem ]; then
    echo "❌ SSL certificates not found. Please place cert.pem and key.pem in nginx/ssl/"
    exit 1
fi

# Load environment variables
export $(cat .env.production | grep -v '^#' | xargs)

# Create backup
echo "💾 Creating backup..."
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U $POSTGRES_USER $POSTGRES_DB > backup_$(date +%Y%m%d_%H%M%S).sql

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down

# Build and start services
echo "🔨 Building and starting services..."
docker-compose -f docker-compose.prod.yml up --build -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 60

# Check service health
echo "🏥 Checking service health..."
docker-compose -f docker-compose.prod.yml ps

# Run database migrations
echo "🗄️ Running database migrations..."
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Initialize MinIO bucket
echo "📦 Initializing MinIO bucket..."
docker-compose -f docker-compose.prod.yml exec minio mc mb /data/laudatorai || true

# Run health checks
echo "🔍 Running health checks..."
curl -f http://localhost/health || {
    echo "❌ Health check failed"
    exit 1
}

echo "✅ Production deployment completed!"
echo "🌐 Application: https://your-domain.com"
echo "📊 Grafana: https://your-domain.com:3001"
echo "📈 Prometheus: https://your-domain.com:9090"
echo "🗄️ MinIO Console: https://your-domain.com:9001"
