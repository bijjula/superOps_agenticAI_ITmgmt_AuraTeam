@echo off
REM Start Service Desk Host Script for Aura Backend (Windows)
REM This script sets up the environment and starts the Service Desk Host

echo 🎫 Starting Aura Service Desk Host...

REM Change to the script directory
cd /d "%~dp0"

REM Check if .env file exists
if not exist ".env" (
    if exist ".env.example" (
        echo ❌ .env file not found. Creating from .env.example...
        copy ".env.example" ".env"
        echo ✅ .env file created. Please update it with your actual configuration.
        echo ⚠️ Make sure to set your OpenAI API key and database URLs
        pause
    ) else (
        echo ❌ Neither .env nor .env.example found
        pause
        exit /b 1
    )
)

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found. Creating one...
    python -m venv venv
    echo ✅ Virtual environment created.
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r service-desk-host\requirements.txt

REM Check if required services are running
echo 🔍 Checking database services...
echo Checking PostgreSQL (port 5432)...
netstat -an | find "5432" >nul
if errorlevel 1 (
    echo ❌ PostgreSQL not detected on port 5432
    echo Please ensure PostgreSQL is running
)

echo Checking MongoDB (port 27017)...
netstat -an | find "27017" >nul
if errorlevel 1 (
    echo ❌ MongoDB not detected on port 27017
    echo Please ensure MongoDB is running
)

echo Checking Redis (port 6379)...
netstat -an | find "6379" >nul
if errorlevel 1 (
    echo ❌ Redis not detected on port 6379
    echo Please ensure Redis is running
)

REM Set PYTHONPATH and start the Service Desk Host
echo 🎯 Starting Service Desk Host...
set PYTHONPATH=.
python service-desk-host\main.py

pause
