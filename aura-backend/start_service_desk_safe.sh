#!/bin/bash

# Aura Service Desk Host Startup Script with Python 3.13 Compatibility
# This script handles the Python 3.13 compatibility issues by trying different approaches

echo "🎫 Starting Aura Service Desk Host (Python 3.13 Safe Mode)..."

# Navigate to aura-backend directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check Python version
echo "🐍 Python version: $(python --version)"

# Try to install dependencies with fallback strategy
echo "📦 Installing dependencies..."

# First, try with minimal requirements that are known to work with Python 3.13
echo "   Step 1: Installing minimal requirements (compatible with Python 3.13)..."
pip install -r requirements_minimal.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install minimal dependencies"
    exit 1
fi

# Try to install asyncpg separately (may fail on Python 3.13)
echo "   Step 2: Attempting to install asyncpg (PostgreSQL async driver)..."
pip install asyncpg>=0.28.0 --no-cache-dir || {
    echo "⚠️  asyncpg failed to install (expected on Python 3.13)"
    echo "   PostgreSQL async features will be limited"
}

# Install additional packages that might work
echo "   Step 3: Installing additional packages..."
pip install aiohttp>=3.8.0 --no-cache-dir || echo "⚠️  aiohttp installation failed"
pip install orjson>=3.8.0 --no-cache-dir || echo "⚠️  orjson installation failed"
pip install starlette>=0.20.0 --no-cache-dir || echo "⚠️  starlette installation failed"

echo "✅ Dependencies installation completed"

# Test core dependencies
echo "🔍 Testing core dependencies..."
python -c "
import sys
failed = []
try:
    import fastapi
    print('✅ FastAPI')
except ImportError as e:
    print(f'❌ FastAPI: {e}')
    failed.append('FastAPI')

try:
    import uvicorn
    print('✅ Uvicorn')
except ImportError as e:
    print(f'❌ Uvicorn: {e}')
    failed.append('Uvicorn')

try:
    import sqlalchemy
    print('✅ SQLAlchemy')
except ImportError as e:
    print(f'❌ SQLAlchemy: {e}')
    failed.append('SQLAlchemy')

try:
    import motor
    print('✅ Motor (MongoDB)')
except ImportError as e:
    print(f'❌ Motor: {e}')
    failed.append('Motor')

try:
    import redis
    print('✅ Redis')
except ImportError as e:
    print(f'❌ Redis: {e}')
    failed.append('Redis')

try:
    import openai
    print('✅ OpenAI')
except ImportError as e:
    print(f'❌ OpenAI: {e}')
    failed.append('OpenAI')

try:
    import pydantic
    print('✅ Pydantic')
except ImportError as e:
    print(f'❌ Pydantic: {e}')
    failed.append('Pydantic')

if failed:
    print(f'\\n❌ Some dependencies failed: {failed}')
    sys.exit(1)
else:
    print('\\n🎉 All core dependencies are working!')
"

if [ $? -ne 0 ]; then
    echo "❌ Dependency test failed"
    exit 1
fi

# Set Python path
export PYTHONPATH=$(pwd):$PYTHONPATH

# Load environment variables from .env file
if [ -f ".env" ]; then
    echo "🔧 Loading environment variables from .env file..."
    set -a  # automatically export all variables
    source .env
    set +a  # stop automatically exporting
else
    echo "❌ .env file not found!"
    exit 1
fi

# Verify critical environment variables
if [ -z "$DATABASE_URL" ]; then
    echo "❌ DATABASE_URL not set!"
    exit 1
fi

if [ -z "$MONGODB_URL" ]; then
    echo "❌ MONGODB_URL not set!"
    exit 1
fi

if [ -z "$REDIS_URL" ]; then
    echo "❌ REDIS_URL not set!"
    exit 1
fi

echo "✅ Environment variables loaded successfully"
echo "📊 Database URLs:"
echo "   PostgreSQL: $DATABASE_URL"
echo "   MongoDB: $MONGODB_URL"
echo "   Redis: $REDIS_URL"

# Navigate to service directory and start
echo "🚀 Starting service..."
cd service-desk-host
python main.py
