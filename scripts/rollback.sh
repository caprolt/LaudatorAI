#!/bin/bash

# LaudatorAI Production Rollback Script
set -e

ENVIRONMENT=${1:-production}
COMPOSE_FILE="docker-compose.${ENVIRONMENT}.yml"

echo "🔄 Starting rollback for ${ENVIRONMENT} environment..."

# Check if compose file exists
if [ ! -f $COMPOSE_FILE ]; then
    echo "❌ $COMPOSE_FILE not found"
    exit 1
fi

# Load environment variables
ENV_FILE=".env.${ENVIRONMENT}"
if [ -f $ENV_FILE ]; then
    export $(cat $ENV_FILE | grep -v '^#' | xargs)
fi

# Stop all services
echo "🛑 Stopping all services..."
docker-compose -f $COMPOSE_FILE down

# Remove containers and images
echo "🧹 Cleaning up containers and images..."
docker-compose -f $COMPOSE_FILE rm -f
docker system prune -f

# Restart with previous version (if available)
echo "🔄 Restarting with previous version..."
docker-compose -f $COMPOSE_FILE up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 30

# Check service health
echo "🏥 Checking service health..."
docker-compose -f $COMPOSE_FILE ps

echo "✅ Rollback completed for ${ENVIRONMENT} environment!"
