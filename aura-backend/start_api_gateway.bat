@echo off
REM Start API Gateway Script for Aura Backend (Windows)
REM This script sets up the environment and starts the API Gateway

echo 🚀 Starting Aura API Gateway...

REM Change to the script directory
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found. Creating one...
    python -m venv venv
    echo ✅ Virtual environment created.
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies if needed
echo 📦 Checking dependencies...
pip install -r api-gateway\requirements.txt >nul 2>&1

REM Set PYTHONPATH and start the API Gateway
echo 🎯 Setting Python path and starting API Gateway...
set PYTHONPATH=.
python api-gateway\main.py

pause
