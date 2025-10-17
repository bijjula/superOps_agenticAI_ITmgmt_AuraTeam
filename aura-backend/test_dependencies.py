#!/usr/bin/env python3
"""
Test script to verify all dependencies are correctly installed
"""

import sys
import importlib

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {package_name or module_name}")
        return True
    except ImportError as e:
        print(f"❌ {package_name or module_name}: {e}")
        return False

def main():
    print("🔍 Testing Python dependencies for Aura Service Desk...")
    print()
    
    # Test core dependencies
    dependencies = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("sqlalchemy", "SQLAlchemy"),
        ("sqlalchemy.ext.asyncio", "SQLAlchemy Async"),
        ("asyncpg", "AsyncPG (PostgreSQL driver)"),
        ("motor", "Motor (MongoDB async driver)"),
        ("redis", "Redis"),
        ("openai", "OpenAI"),
        ("pydantic", "Pydantic"),
        ("httpx", "HTTPX"),
        ("python_dotenv", "Python-dotenv"),
        ("structlog", "Structlog"),
        ("dateutil", "Python-dateutil"),
        ("multipart", "Python-multipart"),
        ("jose", "Python-jose"),
        ("passlib", "Passlib"),
        ("pytest", "Pytest"),
    ]
    
    failed_imports = []
    successful_imports = 0
    
    for module, name in dependencies:
        if test_import(module, name):
            successful_imports += 1
        else:
            failed_imports.append(name)
    
    print()
    print(f"📊 Import Test Results:")
    print(f"   ✅ Successful: {successful_imports}/{len(dependencies)}")
    
    if failed_imports:
        print(f"   ❌ Failed: {len(failed_imports)}")
        print(f"   Failed modules: {', '.join(failed_imports)}")
        print()
        print("🔧 To fix missing dependencies, run:")
        print("   pip install -r requirements.txt")
        return 1
    else:
        print(f"   🎉 All dependencies are correctly installed!")
        return 0

if __name__ == "__main__":
    sys.exit(main())
