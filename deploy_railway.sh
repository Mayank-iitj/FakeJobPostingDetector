#!/bin/bash

# Quick deployment script for Railway

echo "🚀 Deploying Threat Intelligence Platform to Railway..."

# Check if railway CLI is installed
if ! command -v railway &> /dev/null
then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

# Login to Railway
echo "📝 Logging in to Railway..."
railway login

# Link project (or create new)
echo "🔗 Linking Railway project..."
railway link

# Deploy
echo "🚢 Deploying..."
railway up

echo "✅ Deployment complete!"
echo "🌐 Check your Railway dashboard for the live URL"
