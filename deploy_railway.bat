@echo off
REM Quick deployment script for Railway (Windows)

echo 🚀 Deploying Threat Intelligence Platform to Railway...

REM Check if railway CLI is installed
where railway >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Railway CLI not found. Installing...
    npm install -g @railway/cli
)

REM Login to Railway
echo 📝 Logging in to Railway...
railway login

REM Link project
echo 🔗 Linking Railway project...
railway link

REM Deploy
echo 🚢 Deploying...
railway up

echo ✅ Deployment complete!
echo 🌐 Check your Railway dashboard for the live URL
pause
