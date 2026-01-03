#!/bin/bash

# Quick Start Script for Job Scam Detector
# Run this after cloning the repository

echo "========================================="
echo "   Job Scam Detector - Quick Setup"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python --version

if [ $? -ne 0 ]; then
    echo "❌ Python not found. Please install Python 3.8+"
    exit 1
fi

echo "✅ Python found"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Create .env file
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
else
    echo "✅ .env file already exists"
fi
echo ""

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p models/saved_models
mkdir -p data/raw
mkdir -p data/processed
echo "✅ Directories created"
echo ""

# Train initial model
echo "Training initial model with sample data..."
python train_model.py

if [ $? -ne 0 ]; then
    echo "⚠️  Model training failed, but you can still use the rule-based system"
else
    echo "✅ Model trained successfully"
fi
echo ""

echo "========================================="
echo "   Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Start the API server:"
echo "   python backend/main.py"
echo ""
echo "2. In a new terminal, start the web UI:"
echo "   streamlit run frontend/streamlit_app.py"
echo ""
echo "3. For Chrome extension:"
echo "   - Open chrome://extensions/"
echo "   - Enable Developer mode"
echo "   - Click 'Load unpacked'"
echo "   - Select the chrome-extension folder"
echo ""
echo "📚 See README.md for full documentation"
echo ""
