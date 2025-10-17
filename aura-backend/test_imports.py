#!/usr/bin/env python3
"""
Test script to verify all imports and environment setup
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')

print("🧪 Testing Aura Service Desk Environment...")
print(f"Python version: {sys.version}")
print(f"Python path: {sys.path}")

# Test critical imports
try:
    import sqlalchemy
    print(f"✅ SQLAlchemy: {sqlalchemy.__version__}")
    
    from sqlalchemy.ext.asyncio import create_async_engine
    print("✅ SQLAlchemy AsyncIO support available")
    
except ImportError as e:
    print(f"❌ SQLAlchemy import failed: {e}")
    sys.exit(1)

try:
    import motor
    print(f"✅ Motor (MongoDB): {motor.version}")
except ImportError as e:
    print(f"❌ Motor import failed: {e}")
    sys.exit(1)

try:
    import redis
    print(f"✅ Redis: {redis.__version__}")
except ImportError as e:
    print(f"❌ Redis import failed: {e}")
    sys.exit(1)

try:
    import fastapi
    print(f"✅ FastAPI: {fastapi.__version__}")
except ImportError as e:
    print(f"❌ FastAPI import failed: {e}")
    sys.exit(1)

try:
    import openai
    print(f"✅ OpenAI: {openai.__version__}")
except ImportError as e:
    print(f"❌ OpenAI import failed: {e}")
    sys.exit(1)

# Test environment variables
print("\n🔧 Environment Variables:")
env_vars = ['DATABASE_URL', 'MONGODB_URL', 'REDIS_URL', 'OPENAI_API_KEY']
for var in env_vars:
    value = os.getenv(var)
    if value:
        # Hide sensitive parts of API keys
        if 'API_KEY' in var and len(value) > 10:
            display_value = f"{value[:10]}...{value[-4:]}"
        else:
            display_value = value
        print(f"✅ {var}: {display_value}")
    else:
        print(f"❌ {var}: Not set")

print("\n🎯 Testing shared module imports...")
try:
    from shared.utils.database import DatabaseManager
    print("✅ DatabaseManager import successful")
except ImportError as e:
    print(f"❌ DatabaseManager import failed: {e}")
    sys.exit(1)

try:
    from shared.utils.ai_service import get_ai_service
    print("✅ AI service import successful")
except ImportError as e:
    print(f"❌ AI service import failed: {e}")
    sys.exit(1)

print("\n🎉 All tests passed! Environment is ready.")
