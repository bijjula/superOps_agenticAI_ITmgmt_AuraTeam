# Aura API Gateway Startup Guide

This guide explains how to start the Aura API Gateway on different operating systems.

## Quick Start

### Option 1: Universal Python Script (Recommended)
Works on **Windows, macOS, and Linux**:
```bash
cd aura-backend
python start_api_gateway.py
```
or
```bash
cd aura-backend
python3 start_api_gateway.py
```

### Option 2: Platform-Specific Scripts

#### For Windows:
```cmd
cd aura-backend
start_api_gateway.bat
```

#### For macOS/Linux:
```bash
cd aura-backend
./start_api_gateway.sh
```

### Option 3: Manual Method
If you prefer to run manually:

#### Windows:
```cmd
cd aura-backend
python -m venv venv
venv\Scripts\activate.bat
pip install -r api-gateway\requirements.txt
set PYTHONPATH=.
python api-gateway\main.py
```

#### macOS/Linux:
```bash
cd aura-backend
python3 -m venv venv
source venv/bin/activate
pip install -r api-gateway/requirements.txt
export PYTHONPATH=.
python3 api-gateway/main.py
```

## What These Scripts Do

All startup methods automatically:

1. **Create virtual environment** (if it doesn't exist)
2. **Activate the virtual environment**
3. **Install required dependencies** from `requirements.txt`
4. **Set correct PYTHONPATH** (fixes the `shared` module import error)
5. **Start the API Gateway** on `http://0.0.0.0:8000`

## Expected Output

When the API Gateway starts successfully, you'll see:
```
🚀 Starting Aura API Gateway...
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

You may also see warnings about unreachable services (service-desk, infra-talent, threat-intel) - this is normal when those microservices aren't running.

## Troubleshooting

### Import Error: No module named 'shared'
This is fixed by setting `PYTHONPATH=.` which all the startup scripts do automatically.

### Permission Denied (macOS/Linux)
Make the shell script executable:
```bash
chmod +x start_api_gateway.sh
```

### Python Not Found
Make sure Python 3.7+ is installed:
- **Windows**: Download from [python.org](https://python.org)
- **macOS**: `brew install python3` or download from python.org
- **Linux**: `sudo apt install python3` (Ubuntu/Debian) or equivalent

## Stopping the API Gateway

Press `Ctrl+C` in the terminal to stop the server.

## API Documentation

Once running, visit:
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
