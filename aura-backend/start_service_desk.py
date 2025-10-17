#!/usr/bin/env python3
"""
Universal startup script for Aura Service Desk Host
Works on Windows, macOS, and Linux
Handles database dependencies and environment setup
"""

import os
import sys
import subprocess
import platform
import time
import socket
from pathlib import Path

def print_status(message):
    """Print status message with emoji"""
    print(f"🎫 {message}")

def print_error(message):
    """Print error message"""
    print(f"❌ {message}")

def print_warning(message):
    """Print warning message"""
    print(f"⚠️ {message}")

def print_success(message):
    """Print success message"""
    print(f"✅ {message}")

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
        print_error(f"Command failed: {' '.join(command) if isinstance(command, list) else command}")
        if capture_output and e.stdout:
            print(f"Output: {e.stdout}")
        if capture_output and e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_port(host, port):
    """Check if a port is open"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            return result == 0
    except Exception:
        return False

def check_database_services():
    """Check if required database services are running"""
    services = {
        "PostgreSQL": ("localhost", 5432),
        "MongoDB": ("localhost", 27017),
        "Redis": ("localhost", 6379)
    }
    
    print_status("Checking database services...")
    
    all_services_running = True
    for service_name, (host, port) in services.items():
        if check_port(host, port):
            print_success(f"{service_name} is running on {host}:{port}")
        else:
            print_error(f"{service_name} is not running on {host}:{port}")
            all_services_running = False
    
    return all_services_running

def setup_environment_file():
    """Set up environment file"""
    script_dir = Path(__file__).parent.absolute()
    env_file = script_dir / ".env"
    env_example = script_dir / ".env.example"
    
    if not env_file.exists():
        if env_example.exists():
            print_status("Creating .env file from .env.example...")
            try:
                import shutil
                shutil.copy(env_example, env_file)
                print_success(".env file created")
                print_warning("Please update .env file with your actual configuration values")
                return True
            except Exception as e:
                print_error(f"Failed to create .env file: {e}")
                return False
        else:
            print_error(".env.example file not found")
            return False
    else:
        print_success(".env file already exists")
        return True

def check_environment_variables():
    """Check if required environment variables are set"""
    required_vars = [
        "OPENAI_API_KEY",
        "DATABASE_URL",
        "MONGODB_URL", 
        "REDIS_URL"
    ]
    
    # Try to load from .env file
    env_file = Path(__file__).parent.absolute() / ".env"
    if env_file.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file)
        except ImportError:
            print_warning("python-dotenv not installed, cannot load .env file")
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print_error("Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease set these variables in your .env file or environment")
        return False
    
    print_success("All required environment variables are set")
    return True

def provide_database_setup_instructions():
    """Provide instructions for setting up databases"""
    print("\n" + "="*60)
    print("DATABASE SETUP INSTRUCTIONS")
    print("="*60)
    
    print("\n🐘 PostgreSQL Setup:")
    if platform.system() == "Darwin":  # macOS
        print("  brew install postgresql")
        print("  brew services start postgresql")
        print("  createdb aura_servicedesk")
    elif platform.system() == "Linux":
        print("  sudo apt-get install postgresql postgresql-contrib")
        print("  sudo systemctl start postgresql")
        print("  sudo -u postgres createdb aura_servicedesk")
    else:  # Windows
        print("  Download and install from: https://www.postgresql.org/download/windows/")
        print("  Create database 'aura_servicedesk' using pgAdmin or psql")
    
    print("\n🍃 MongoDB Setup:")
    if platform.system() == "Darwin":  # macOS
        print("  brew tap mongodb/brew")
        print("  brew install mongodb-community")
        print("  brew services start mongodb-community")
    elif platform.system() == "Linux":
        print("  Follow instructions at: https://docs.mongodb.com/manual/installation/")
        print("  sudo systemctl start mongod")
    else:  # Windows
        print("  Download from: https://www.mongodb.com/try/download/community")
        print("  Install and start MongoDB service")
    
    print("\n🔴 Redis Setup:")
    if platform.system() == "Darwin":  # macOS
        print("  brew install redis")
        print("  brew services start redis")
    elif platform.system() == "Linux":
        print("  sudo apt-get install redis-server")
        print("  sudo systemctl start redis-server")
    else:  # Windows
        print("  Download from: https://github.com/microsoftarchive/redis/releases")
        print("  Or use Docker: docker run -d -p 6379:6379 redis:latest")
    
    print("\n🔑 OpenAI API Key:")
    print("  1. Go to https://platform.openai.com/api-keys")
    print("  2. Create a new API key")
    print("  3. Set OPENAI_API_KEY in your .env file")
    
    print("\n🐳 Alternative: Use Docker Compose")
    print("  docker-compose up -d  # Start all services with Docker")
    
    print("="*60)

def main():
    """Main startup function"""
    print_status("Starting Aura Service Desk Host...")
    
    # Change to script directory
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    print(f"📁 Working directory: {script_dir}")
    
    # Detect OS
    os_type = platform.system()
    print(f"💻 Detected OS: {os_type}")
    
    # Setup environment file
    if not setup_environment_file():
        return False
    
    # Check environment variables
    if not check_environment_variables():
        print_warning("Environment variables not properly configured")
        print("Please update your .env file with the correct values")
        return False
    
    # Check database services
    if not check_database_services():
        print_error("Required database services are not running")
        provide_database_setup_instructions()
        print("\nPlease start the required services and try again.")
        return False
    
    # Virtual environment paths
    if os_type == "Windows":
        venv_dir = script_dir / "venv"
        venv_python = venv_dir / "Scripts" / "python.exe"
        venv_pip = venv_dir / "Scripts" / "pip.exe"
    else:  # macOS/Linux
        venv_dir = script_dir / "venv"
        venv_python = venv_dir / "bin" / "python"
        venv_pip = venv_dir / "bin" / "pip"
    
    # Check if virtual environment exists
    if not venv_dir.exists():
        print_status("Virtual environment not found. Creating one...")
        if not run_command([sys.executable, "-m", "venv", str(venv_dir)]):
            print_error("Failed to create virtual environment")
            return False
        print_success("Virtual environment created.")
    
    # Check if Python exists in venv
    if not venv_python.exists():
        print_status("Virtual environment appears corrupted. Recreating...")
        import shutil
        shutil.rmtree(venv_dir)
        if not run_command([sys.executable, "-m", "venv", str(venv_dir)]):
            print_error("Failed to create virtual environment")
            return False
        print_success("Virtual environment recreated.")
    
    # Install dependencies
    print_status("Installing/checking dependencies...")
    requirements_file = script_dir / "service-desk-host" / "requirements.txt"
    
    if requirements_file.exists():
        install_cmd = [str(venv_pip), "install", "-r", str(requirements_file)]
        if not run_command(install_cmd):
            print_error("Failed to install dependencies")
            return False
        print_success("Dependencies ready.")
    else:
        print_warning("Requirements file not found, skipping dependency installation")
    
    # Set environment variables
    env = os.environ.copy()
    env["PYTHONPATH"] = str(script_dir)
    
    # Load .env file variables into environment
    env_file = script_dir / ".env"
    if env_file.exists():
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env[key.strip()] = value.strip()
        except Exception as e:
            print_warning(f"Error loading .env file: {e}")
    
    # Start the Service Desk Host
    print_status("Starting Service Desk Host...")
    main_script = script_dir / "service-desk-host" / "main.py"
    
    if not main_script.exists():
        print_error(f"Main script not found: {main_script}")
        return False
    
    print_success("Service Desk Host is starting on http://0.0.0.0:8001")
    print("Press Ctrl+C to stop the service")
    print("-" * 50)
    
    # Run the Service Desk Host
    try:
        subprocess.run([str(venv_python), str(main_script)], 
                      env=env, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Service Desk Host stopped by user")
    except subprocess.CalledProcessError as e:
        print_error(f"Service Desk Host failed with exit code: {e.returncode}")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Failed to start Service Desk Host")
            sys.exit(1)
    except Exception as e:
        print_error(f"Fatal error: {e}")
        sys.exit(1)
