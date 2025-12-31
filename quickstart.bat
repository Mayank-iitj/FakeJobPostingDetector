@echo off
REM Quick start script for Windows

echo 🛡️ Threat Intelligence Platform - Quick Start
echo.

REM Check Python version
python --version 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python not found. Please install Python 3.10+
    pause
    exit /b 1
)

echo ✅ Python detected

REM Create virtual environment
if not exist venv (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Upgrade pip
echo 📦 Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Create .env file
if not exist .env (
    echo 📝 Creating .env file...
    copy .env.example .env
    echo ⚠️  Please edit .env with your configuration
)

REM Create directories
if not exist data\phishing mkdir data\phishing
if not exist data\malware mkdir data\malware
if not exist data\screenshots mkdir data\screenshots
if not exist models\checkpoints mkdir models\checkpoints
if not exist logs mkdir logs

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Edit .env with your configuration
echo 2. Start API: python -m api.main
echo 3. Start Gradio UI: python ui\gradio_app.py
echo 4. Access docs: http://localhost:8000/docs
echo.
pause
