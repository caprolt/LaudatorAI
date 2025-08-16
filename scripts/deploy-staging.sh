#!/bin/bash

# LaudatorAI Staging Deployment Script
set -e

echo "🚀 Starting LaudatorAI staging deployment..."

# Check if .env.staging exists
if [ ! -f .env.staging ]; then
    echo "❌ .env.staging file not found. Please copy .env.staging.template and configure it."
    exit 1
fi

# Load environment variables
export $(cat .env.staging | grep -v '^#' | xargs)

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.staging.yml down

# Build and start services
echo "🔨 Building and starting services..."
docker-compose -f docker-compose.staging.yml up --build -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 30

# Check service health
echo "🏥 Checking service health..."
docker-compose -f docker-compose.staging.yml ps

# Run database migrations
echo "🗄️ Running database migrations..."
docker-compose -f docker-compose.staging.yml exec backend alembic upgrade head

# Initialize MinIO bucket
echo "📦 Initializing MinIO bucket..."
docker-compose -f docker-compose.staging.yml exec minio mc mb /data/laudatorai_staging || true

echo "✅ Staging deployment completed!"
echo "🌐 Frontend: http://localhost:3002"
echo "🔧 Backend API: http://localhost:8001"
echo "📊 Grafana: http://localhost:3003"
echo "📈 Prometheus: http://localhost:9091"
echo "🗄️ MinIO Console: http://localhost:9003"
