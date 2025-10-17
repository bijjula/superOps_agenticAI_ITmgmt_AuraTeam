#!/bin/bash

# Start API Gateway Script for Aura Backend
# This script sets up the environment and starts the API Gateway

echo "🚀 Starting Aura API Gateway..."

# Change to the aura-backend directory
cd "$(dirname "$0")"

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
echo "📦 Checking dependencies..."
pip install -r api-gateway/requirements.txt > /dev/null 2>&1

# Set PYTHONPATH and start the API Gateway
echo "🎯 Setting Python path and starting API Gateway..."
export PYTHONPATH=.
python3 api-gateway/main.py
