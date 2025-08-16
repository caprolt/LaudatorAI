#!/bin/bash

# LaudatorAI Load Testing Script
set -e

ENVIRONMENT=${1:-staging}
BASE_URL=${2:-http://localhost:8001}

echo "🧪 Starting load test for ${ENVIRONMENT} environment..."

# Check if required tools are installed
if ! command -v curl &> /dev/null; then
    echo "❌ curl is required but not installed"
    exit 1
fi

# Create test data
echo "📝 Creating test data..."
TEST_JOB_URL="https://example.com/job-posting"
TEST_RESUME_PATH="test_resume.pdf"

# Function to test job extraction
test_job_extraction() {
    echo "🔍 Testing job extraction endpoint..."
    for i in {1..10}; do
        curl -X POST "${BASE_URL}/api/v1/jobs/extract" \
            -H "Content-Type: application/json" \
            -d "{\"url\": \"${TEST_JOB_URL}\"}" \
            -w "Job extraction $i: %{http_code} %{time_total}s\n" \
            -o /dev/null -s &
    done
    wait
}

# Function to test health endpoint
test_health_endpoint() {
    echo "🏥 Testing health endpoint..."
    for i in {1..50}; do
        curl -f "${BASE_URL}/health" \
            -w "Health check $i: %{http_code} %{time_total}s\n" \
            -o /dev/null -s &
    done
    wait
}

# Function to test concurrent users
test_concurrent_users() {
    echo "👥 Testing concurrent users..."
    for i in {1..20}; do
        (
            # Simulate user session
            curl -f "${BASE_URL}/health" -o /dev/null -s
            sleep 0.1
            curl -X POST "${BASE_URL}/api/v1/jobs/extract" \
                -H "Content-Type: application/json" \
                -d "{\"url\": \"${TEST_JOB_URL}\"}" \
                -o /dev/null -s
        ) &
    done
    wait
}

# Run tests
echo "🚀 Starting load tests..."

echo "=== Test 1: Health Endpoint Load ==="
test_health_endpoint

echo "=== Test 2: Job Extraction Load ==="
test_job_extraction

echo "=== Test 3: Concurrent Users ==="
test_concurrent_users

echo "✅ Load testing completed!"
echo "📊 Check the monitoring dashboard for detailed metrics"
