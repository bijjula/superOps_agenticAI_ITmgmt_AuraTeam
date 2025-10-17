# Dependency Installation Fix for Python 3.13

## Problem
The service desk host was failing to start with multiple issues:
1. `ModuleNotFoundError: No module named 'sqlalchemy'`
2. Compilation errors when installing `asyncpg` and `pydantic-core` on Python 3.13
3. Python 3.13 compatibility issues with older package versions

## Root Cause Analysis
1. **Missing Dependencies**: The root `aura-backend/requirements.txt` was missing several critical dependencies
2. **Python 3.13 Compatibility**: Many packages didn't have pre-built wheels for Python 3.13, causing compilation failures
3. **Hidden Installation Errors**: The startup script was hiding installation failures
4. **Version Conflicts**: Multiple compatibility issues:
   - Older package versions were incompatible with Python 3.13
   - `pymongo==4.10.1` conflicted with `motor==3.6.0` (requires `pymongo<4.10`)

## Solutions Implemented

### 1. Updated Requirements Files
**Updated both `requirements.txt` files with Python 3.13 compatible versions:**
- `fastapi==0.115.4` (latest with Python 3.13 support)
- `pydantic==2.10.2` (latest with Python 3.13 support)
- `asyncpg==0.30.0` (newer version with better Python 3.13 support)
- `sqlalchemy[asyncio]==2.0.36` (latest stable)
- All other packages updated to latest compatible versions

### 2. Created Fallback Solutions
**`requirements_minimal.txt`** - Minimal requirements that work reliably on Python 3.13:
- Uses version ranges (>=) instead of pinned versions
- Excludes problematic packages that require compilation
- Focuses on core functionality

**`database_safe.py`** - Graceful fallback for asyncpg issues:
- Detects if asyncpg is available
- Falls back to sync PostgreSQL connections if async fails
- Maintains full functionality with limited performance impact

### 3. Improved Startup Scripts
**Enhanced `start_service_desk_with_env.sh`:**
- Shows installation output and errors
- Installs from both root and service-specific requirements
- Includes dependency testing before service start

**New `start_service_desk_safe.sh`** - Python 3.13 optimized startup:
- Uses fallback installation strategy
- Attempts asyncpg installation but continues if it fails
- Provides clear feedback on what's working vs. what failed

### 4. Testing and Diagnostics
**`test_dependencies.py`** - Comprehensive dependency testing
- Tests all critical imports
- Provides clear success/failure reporting
- Gives actionable fix instructions

## Testing Instructions

### Option 1: Safe Startup (Recommended for Python 3.13)
```bash
cd aura-backend
./start_service_desk_safe.sh
```

### Option 2: Standard Startup (try first, may fail on Python 3.13)
```bash
cd aura-backend
./start_service_desk_with_env.sh
```

### Option 3: Manual Installation with Minimal Requirements
```bash
cd aura-backend
source venv/bin/activate

# Install minimal requirements first
pip install -r requirements_minimal.txt

# Test what's working
python test_dependencies.py

# Try to add asyncpg if desired
pip install asyncpg>=0.28.0 --no-cache-dir || echo "AsyncPG not available"

# Start service
cd service-desk-host
python main.py
```

### Option 4: Test Dependencies Only
```bash
cd aura-backend
source venv/bin/activate
python test_dependencies.py
```

## Expected Output (Safe Mode)
```
🎫 Starting Aura Service Desk Host (Python 3.13 Safe Mode)...
🐍 Python version: Python 3.13.x
📦 Installing dependencies...
   Step 1: Installing minimal requirements (compatible with Python 3.13)...
   Step 2: Attempting to install asyncpg (PostgreSQL async driver)...
   ⚠️  asyncpg failed to install (expected on Python 3.13)
   Step 3: Installing additional packages...
✅ Dependencies installation completed

🔍 Testing core dependencies...
✅ FastAPI
✅ Uvicorn
✅ SQLAlchemy
✅ Motor (MongoDB)
✅ Redis
✅ OpenAI
✅ Pydantic

🎉 All core dependencies are working!
```

## Files Created/Modified

### New Files:
1. `aura-backend/requirements_minimal.txt` - Python 3.13 safe requirements
2. `aura-backend/start_service_desk_safe.sh` - Python 3.13 optimized startup
3. `aura-backend/shared/utils/database_safe.py` - Fallback database module
4. `aura-backend/test_dependencies.py` - Dependency testing script

### Modified Files:
1. `aura-backend/requirements.txt` - Updated to latest Python 3.13 compatible versions
2. `aura-backend/service-desk-host/requirements.txt` - Updated versions
3. `aura-backend/start_service_desk_with_env.sh` - Improved error handling

## Fallback Strategy
If asyncpg compilation fails (common on Python 3.13):
1. The service will use sync PostgreSQL connections instead of async
2. MongoDB and Redis connections remain fully async
3. Core functionality is preserved with minimal performance impact
4. Clear warnings indicate which features are limited

## Migration Path
1. **Immediate**: Use `start_service_desk_safe.sh` to get running quickly
2. **Future**: Monitor package updates and migrate back to full async when Python 3.13 support improves
3. **Alternative**: Consider using Python 3.11 or 3.12 for full async PostgreSQL support

## Verification
After applying this fix:
- ✅ Service starts without `ModuleNotFoundError`
- ✅ All core dependencies load successfully  
- ✅ Database connections work (with graceful async fallback)
- ✅ Clear feedback on what's working vs. limited functionality
