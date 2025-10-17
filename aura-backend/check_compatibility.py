#!/usr/bin/env python3
"""
Quick compatibility check for package versions
"""

def check_motor_pymongo_compatibility():
    """Check if motor and pymongo versions are compatible"""
    print("🔍 Checking package version compatibility...")
    
    # Known compatibility matrix
    compatibility = {
        "motor==3.6.0": "pymongo>=4.9,<4.10",
        "motor==3.5.1": "pymongo>=4.8,<4.10", 
        "motor==3.4.0": "pymongo>=4.5,<4.8",
    }
    
    current_versions = {
        "motor": "3.6.0",
        "pymongo": "4.9.1"
    }
    
    print(f"Current versions:")
    print(f"  motor: {current_versions['motor']}")
    print(f"  pymongo: {current_versions['pymongo']}")
    
    # Check compatibility
    motor_key = f"motor=={current_versions['motor']}"
    if motor_key in compatibility:
        required_pymongo = compatibility[motor_key]
        print(f"\nCompatibility check:")
        print(f"  motor {current_versions['motor']} requires: {required_pymongo}")
        
        # Parse version
        pymongo_version = current_versions['pymongo']
        version_parts = [int(x) for x in pymongo_version.split('.')]
        
        # Check if 4.9.1 is in range [4.9, 4.10)
        if version_parts[0] == 4 and version_parts[1] == 9:
            print(f"  ✅ pymongo {pymongo_version} is compatible!")
            return True
        else:
            print(f"  ❌ pymongo {pymongo_version} is NOT compatible!")
            return False
    else:
        print(f"  ⚠️  Unknown compatibility for motor {current_versions['motor']}")
        return False

def check_python_version():
    """Check Python version and show recommendations"""
    import sys
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"\n🐍 Python version: {python_version}")
    
    if sys.version_info >= (3, 13):
        print("  ⚠️  Python 3.13+ detected - some packages may need compilation")
        print("  💡 Recommendation: Use the safe startup script")
        return "3.13+"
    elif sys.version_info >= (3, 11):
        print("  ✅ Python 3.11-3.12 - good compatibility with most packages")
        return "3.11-3.12"
    else:
        print("  ⚠️  Python < 3.11 - consider upgrading for better compatibility")
        return "old"

def main():
    print("🔧 Aura Backend Compatibility Check")
    print("=" * 40)
    
    python_status = check_python_version()
    compatibility_ok = check_motor_pymongo_compatibility()
    
    print("\n📋 Summary:")
    if compatibility_ok:
        print("  ✅ Package versions are compatible")
    else:
        print("  ❌ Package version conflicts detected")
    
    print("\n💡 Recommended next steps:")
    if python_status == "3.13+":
        print("  1. Use: ./start_service_desk_safe.sh")
        print("  2. Or install minimal requirements first")
    else:
        print("  1. Try: ./start_service_desk_with_env.sh")
        print("  2. Fallback: ./start_service_desk_safe.sh")
    
    return 0 if compatibility_ok else 1

if __name__ == "__main__":
    exit(main())
