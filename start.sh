#!/bin/bash

# Railway Startup Script for Threat Intelligence Platform

echo "🛡️ Starting Threat Intelligence Platform..."

# Create necessary directories
mkdir -p data/phishing data/malware data/screenshots models/checkpoints logs

# Set default environment variables if not provided
export API_HOST=${API_HOST:-0.0.0.0}
export API_PORT=${PORT:-8000}
export LOG_LEVEL=${LOG_LEVEL:-info}
export WORKERS=${WORKERS:-4}

echo "✅ Environment configured"
echo "📍 Host: $API_HOST:$API_PORT"
echo "👷 Workers: $WORKERS"

# Start the application
echo "🚀 Starting API server..."
exec uvicorn api.main:app \
    --host $API_HOST \
    --port $API_PORT \
    --workers $WORKERS \
    --log-level $LOG_LEVEL \
    --access-log \
    --proxy-headers \
    --forwarded-allow-ips='*'
