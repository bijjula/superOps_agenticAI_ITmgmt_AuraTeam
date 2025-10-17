#!/usr/bin/env python3
"""
Universal startup script for Aura API Gateway
Works on Windows, macOS, and Linux
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_status(message):
    """Print status message with emoji"""
    print(f"🚀 {message}")

def run_command(command, shell=False, check=True, capture_output=False):
    """Run a command with proper error handling"""
    try:
        if capture_output:
            result = subprocess.run(command, shell=shell, check=check, 
                                  capture_output=True, text=True)
            return result.stdout.strip()
        else:
            subprocess.run(command, shell=shell, check=check)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {' '.join(command) if isinstance(command, list) else command}")
        print(f"Error: {e}")
        return False

def main():
    """Main startup function"""
    print_status("Starting Aura API Gateway...")
    
    # Change to script directory
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    print(f"📁 Working directory: {script_dir}")
    
    # Detect OS
    os_type = platform.system()
    print(f"💻 Detected OS: {os_type}")
    
    # Virtual environment paths
    if os_type == "Windows":
        venv_dir = script_dir / "venv"
        venv_python = venv_dir / "Scripts" / "python.exe"
        venv_pip = venv_dir / "Scripts" / "pip.exe"
        activate_script = venv_dir / "Scripts" / "activate.bat"
    else:  # macOS/Linux
        venv_dir = script_dir / "venv"
        venv_python = venv_dir / "bin" / "python"
        venv_pip = venv_dir / "bin" / "pip"
        activate_script = venv_dir / "bin" / "activate"
    
    # Check if virtual environment exists
    if not venv_dir.exists():
        print("❌ Virtual environment not found. Creating one...")
        if not run_command([sys.executable, "-m", "venv", str(venv_dir)]):
            print("Failed to create virtual environment")
            return False
        print("✅ Virtual environment created.")
    
    # Check if Python exists in venv
    if not venv_python.exists():
        print("❌ Virtual environment appears corrupted. Recreating...")
        import shutil
        shutil.rmtree(venv_dir)
        if not run_command([sys.executable, "-m", "venv", str(venv_dir)]):
            print("Failed to create virtual environment")
            return False
        print("✅ Virtual environment recreated.")
    
    # Install dependencies
    print("📦 Installing/checking dependencies...")
    requirements_file = script_dir / "api-gateway" / "requirements.txt"
    
    if requirements_file.exists():
        install_cmd = [str(venv_pip), "install", "-r", str(requirements_file)]
        if not run_command(install_cmd):
            print("Failed to install dependencies")
            return False
        print("✅ Dependencies ready.")
    else:
        print("⚠️ Requirements file not found, skipping dependency installation")
    
    # Set environment variables
    env = os.environ.copy()
    env["PYTHONPATH"] = str(script_dir)
    
    # Start the API Gateway
    print("🎯 Starting API Gateway...")
    main_script = script_dir / "api-gateway" / "main.py"
    
    if not main_script.exists():
        print(f"❌ Main script not found: {main_script}")
        return False
    
    # Run the API Gateway
    try:
        subprocess.run([str(venv_python), str(main_script)], 
                      env=env, check=True)
    except KeyboardInterrupt:
        print("\n🛑 API Gateway stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ API Gateway failed with exit code: {e.returncode}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Failed to start API Gateway")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
