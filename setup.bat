@echo off
REM Quick Start Script for Job Scam Detector (Windows)
REM Run this after cloning the repository

echo =========================================
echo    Job Scam Detector - Quick Setup
echo =========================================
echo.

REM Check Python version
echo Checking Python version...
python --version

if errorlevel 1 (
    echo X Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

echo + Python found
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

if errorlevel 1 (
    echo X Failed to create virtual environment
    pause
    exit /b 1
)

echo + Virtual environment created
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo X Failed to activate virtual environment
    pause
    exit /b 1
)

echo + Virtual environment activated
echo.

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo X Failed to install dependencies
    pause
    exit /b 1
)

echo + Dependencies installed
echo.

REM Create .env file
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo + .env file created
) else (
    echo + .env file already exists
)
echo.

REM Create necessary directories
echo Creating necessary directories...
if not exist models\saved_models mkdir models\saved_models
if not exist data\raw mkdir data\raw
if not exist data\processed mkdir data\processed
echo + Directories created
echo.

REM Train initial model
echo Training initial model with sample data...
python train_model.py

if errorlevel 1 (
    echo ! Model training failed, but you can still use the rule-based system
) else (
    echo + Model trained successfully
)
echo.

echo =========================================
echo    Setup Complete!
echo =========================================
echo.
echo Next steps:
echo.
echo 1. Start the API server:
echo    python backend\main.py
echo.
echo 2. In a new terminal, start the web UI:
echo    streamlit run frontend\streamlit_app.py
echo.
echo 3. For Chrome extension:
echo    - Open chrome://extensions/
echo    - Enable Developer mode
echo    - Click 'Load unpacked'
echo    - Select the chrome-extension folder
echo.
echo See README.md for full documentation
echo.
pause
