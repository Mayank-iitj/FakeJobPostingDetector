@echo off
REM Railway Quick Deploy Script for Windows

echo.
echo ============================================================
echo   Threat Intelligence Platform - Railway Deployment
echo ============================================================
echo.

REM Check if Railway CLI is installed
where railway >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Railway CLI not found. Installing...
    npm install -g @railway/cli
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo ERROR: Failed to install Railway CLI
        echo Please install Node.js first: https://nodejs.org
        pause
        exit /b 1
    )
)

echo Railway CLI detected
echo.

REM Check if logged in
railway whoami >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Please login to Railway...
    railway login
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo ERROR: Railway login failed
        pause
        exit /b 1
    )
)

echo.
echo Logged in to Railway
echo.

REM Check if project is linked
if not exist .railway (
    echo No Railway project linked. Creating new project...
    railway init
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo ERROR: Failed to initialize Railway project
        pause
        exit /b 1
    )
) else (
    echo Railway project already linked
)

echo.
echo ============================================================
echo   Deploying to Railway...
echo ============================================================
echo.

railway up

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo   Deployment Successful!
    echo ============================================================
    echo.
    echo Next steps:
    echo 1. Set environment variables in Railway dashboard
    echo 2. Add custom domain ^(optional^)
    echo 3. Test your API:
    echo    railway open
    echo.
    echo View logs:
    echo    railway logs
    echo.
) else (
    echo.
    echo ============================================================
    echo   Deployment Failed
    echo ============================================================
    echo.
    echo Check the error messages above
    echo View full logs: railway logs
    echo.
)

pause
