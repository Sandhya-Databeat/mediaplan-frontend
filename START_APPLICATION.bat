@echo off
echo ========================================
echo   Spotify Media Plan - Quick Start
echo ========================================
echo.
echo This will start both Backend and Frontend
echo.

REM Check if backend is already running
echo [1/3] Checking if backend is already running...
curl -s http://localhost:8000/health > nul 2>&1
if %errorlevel% equ 0 (
    echo     ✓ Backend is already running!
) else (
    echo     ✗ Backend is not running
    echo.
    echo [2/3] Starting Backend...
    echo     Opening new window for FastAPI backend...
    start "Spotify Backend - FastAPI" cmd /k "cd /d C:\Users\user\Desktop\backend folder - Copy\spotify-report-studio-backend && run.bat"

    echo     Waiting 10 seconds for backend to start...
    timeout /t 10 /nobreak > nul
)

echo.
echo [3/3] Starting Frontend...
echo     Opening Streamlit in your browser...
cd /d "C:\Users\user\Desktop\MediaPlan - Frontend"
streamlit run media_plan_form_streamlit.py

pause
