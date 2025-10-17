#!/bin/bash

# Start Service Desk Host Script for Aura Backend (Mac/Linux)
# This script sets up the environment and starts the Service Desk Host

echo "🎫 Starting Aura Service Desk Host..."

# Change to the script directory
cd "$(dirname "$0")"

# Function to check if a port is open
check_port() {
    local host=$1
    local port=$2
    nc -z $host $port 2>/dev/null
    return $?
}

# Check if .env file exists
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "❌ .env file not found. Creating from .env.example..."
        cp ".env.example" ".env"
        echo "✅ .env file created. Please update it with your actual configuration."
        echo "⚠️ Make sure to set your OpenAI API key and database URLs"
        echo "Press any key to continue..."
        read -n 1
    else
        echo "❌ Neither .env nor .env.example found"
        exit 1
    fi
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "✅ Virtual environment created."
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
echo "📦 Installing dependencies..."
pip install -r service-desk-host/requirements.txt > /dev/null 2>&1

# Check if required services are running
echo "🔍 Checking database services..."

echo "Checking PostgreSQL (port 5432)..."
if check_port localhost 5432; then
    echo "✅ PostgreSQL is running"
else
    echo "❌ PostgreSQL not detected on port 5432"
    echo "Please ensure PostgreSQL is running"
fi

echo "Checking MongoDB (port 27017)..."
if check_port localhost 27017; then
    echo "✅ MongoDB is running"
else
    echo "❌ MongoDB not detected on port 27017"
    echo "Please ensure MongoDB is running"
fi

echo "Checking Redis (port 6379)..."
if check_port localhost 6379; then
    echo "✅ Redis is running"
else
    echo "❌ Redis not detected on port 6379"
    echo "Please ensure Redis is running"
fi

# Provide setup instructions if services are missing
if ! (check_port localhost 5432 && check_port localhost 27017 && check_port localhost 6379); then
    echo ""
    echo "⚠️ Some required services are not running. Here's how to start them:"
    echo ""
    
    # Detect OS for specific instructions
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        echo "📱 macOS Setup:"
        echo "  PostgreSQL: brew install postgresql && brew services start postgresql"
        echo "  MongoDB:    brew tap mongodb/brew && brew install mongodb-community && brew services start mongodb-community"
        echo "  Redis:      brew install redis && brew services start redis"
    else
        # Linux
        echo "🐧 Linux Setup:"
        echo "  PostgreSQL: sudo apt-get install postgresql && sudo systemctl start postgresql"
        echo "  MongoDB:    Follow https://docs.mongodb.com/manual/installation/"
        echo "  Redis:      sudo apt-get install redis-server && sudo systemctl start redis-server"
    fi
    
    echo ""
    echo "🐳 Alternative: Use Docker Compose"
    echo "  docker-compose up -d"
    echo ""
    echo "Press any key to continue anyway, or Ctrl+C to abort..."
    read -n 1
fi

# Set PYTHONPATH and start the Service Desk Host
echo "🎯 Starting Service Desk Host..."
export PYTHONPATH=.

echo "✅ Service Desk Host is starting on http://0.0.0.0:8001"
echo "Press Ctrl+C to stop the service"
echo "================================================"

python3 service-desk-host/main.py
