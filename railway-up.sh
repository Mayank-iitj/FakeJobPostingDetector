#!/bin/bash

# Railway Quick Deploy Script for Linux/Mac

set -e  # Exit on error

echo ""
echo "============================================================"
echo "  Threat Intelligence Platform - Railway Deployment"
echo "============================================================"
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "Railway CLI not found. Installing..."
    npm install -g @railway/cli
    
    if [ $? -ne 0 ]; then
        echo ""
        echo "ERROR: Failed to install Railway CLI"
        echo "Please install Node.js first: https://nodejs.org"
        exit 1
    fi
fi

echo "✅ Railway CLI detected"
echo ""

# Check if logged in
if ! railway whoami &> /dev/null; then
    echo "Please login to Railway..."
    railway login
    
    if [ $? -ne 0 ]; then
        echo ""
        echo "ERROR: Railway login failed"
        exit 1
    fi
fi

echo "✅ Logged in to Railway"
echo ""

# Check if project is linked
if [ ! -d ".railway" ]; then
    echo "No Railway project linked. Creating new project..."
    railway init
    
    if [ $? -ne 0 ]; then
        echo ""
        echo "ERROR: Failed to initialize Railway project"
        exit 1
    fi
else
    echo "✅ Railway project already linked"
fi

echo ""
echo "============================================================"
echo "  Deploying to Railway..."
echo "============================================================"
echo ""

railway up

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo "  ✅ Deployment Successful!"
    echo "============================================================"
    echo ""
    echo "Next steps:"
    echo "1. Set environment variables in Railway dashboard"
    echo "2. Add custom domain (optional)"
    echo "3. Test your API:"
    echo "   railway open"
    echo ""
    echo "View logs:"
    echo "   railway logs"
    echo ""
else
    echo ""
    echo "============================================================"
    echo "  ❌ Deployment Failed"
    echo "============================================================"
    echo ""
    echo "Check the error messages above"
    echo "View full logs: railway logs"
    echo ""
    exit 1
fi
