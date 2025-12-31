@echo off
REM Render Pre-Deployment Check Script for Windows
REM Verifies your app is ready for Render deployment

echo ======================================================================
echo 🚀 RENDER DEPLOYMENT PRE-CHECK
echo ======================================================================
echo.

set ALL_GOOD=1

REM Check required files
echo 📁 CHECKING REQUIRED FILES:
echo ----------------------------------------------------------------------

set REQUIRED_FILES=render.yaml requirements.txt runtime.txt api\main.py api\routes\phishing.py api\routes\malware.py api\routes\auth.py

for %%f in (%REQUIRED_FILES%) do (
    if exist %%f (
        echo ✅ %%f
    ) else (
        echo ❌ %%f - MISSING
        set ALL_GOOD=0
    )
)

echo.

REM Check optional files
echo 📄 CHECKING OPTIONAL FILES:
echo ----------------------------------------------------------------------

set OPTIONAL_FILES=.env.render .gitignore RENDER_DEPLOY.md RENDER_ENV_SETUP.md

for %%f in (%OPTIONAL_FILES%) do (
    if exist %%f (
        echo ✅ %%f
    ) else (
        echo ⚠️  %%f
    )
)

echo.

REM Check Python version
echo 🐍 PYTHON VERSION:
echo ----------------------------------------------------------------------
if exist runtime.txt (
    type runtime.txt
    echo ✅ Runtime configured
) else (
    echo ⚠️  runtime.txt not found
)

echo.

REM Check dependencies
echo 📦 CHECKING DEPENDENCIES:
echo ----------------------------------------------------------------------
findstr /C:"torch" requirements.txt >nul 2>&1 && echo ✅ PyTorch found
findstr /C:"transformers" requirements.txt >nul 2>&1 && echo ✅ Transformers found
findstr /C:"fastapi" requirements.txt >nul 2>&1 && echo ✅ FastAPI found
findstr /C:"uvicorn" requirements.txt >nul 2>&1 && echo ✅ Uvicorn found

echo.

REM Check render.yaml
echo ⚙️  CHECKING RENDER CONFIGURATION:
echo ----------------------------------------------------------------------
if exist render.yaml (
    echo ✅ render.yaml found
    findstr /C:"buildCommand" render.yaml >nul 2>&1 && echo ✅ Build command configured
    findstr /C:"startCommand" render.yaml >nul 2>&1 && echo ✅ Start command configured
    findstr /C:"SECRET_KEY" render.yaml >nul 2>&1 && echo ✅ SECRET_KEY configured
) else (
    echo ⚠️  render.yaml not found
)

echo.

REM Final summary
echo ======================================================================
if %ALL_GOOD%==1 (
    echo ✅ ALL CRITICAL CHECKS PASSED!
    echo.
    echo 🚀 READY TO DEPLOY TO RENDER!
    echo.
    echo Next Steps:
    echo 1. Push code to GitHub
    echo 2. Go to render.com and sign up/login
    echo 3. Click 'New +' -^> 'Web Service'
    echo 4. Connect your GitHub repository
    echo 5. Deploy!
    echo.
    echo 📖 Read RENDER_DEPLOY.md for detailed instructions
) else (
    echo ❌ SOME CHECKS FAILED
    echo Fix missing required files before deploying
    exit /b 1
)
echo ======================================================================

pause
