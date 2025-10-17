#!/bin/bash

# Aura Service Desk Host Startup Script with Environment Loading
# This script properly loads environment variables and starts the service

echo "🎫 Starting Aura Service Desk Host..."

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

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r service-desk-host/requirements.txt > /dev/null 2>&1

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
