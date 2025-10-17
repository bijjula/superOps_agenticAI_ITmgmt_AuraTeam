#!/usr/bin/env python3
"""
Robust service startup script for Aura Backend Services
Handles dependencies, health checks, and graceful failure recovery
"""

import os
import sys
import time
import subprocess
import threading
import signal
import json
import requests
from typing import Dict, List, Optional
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

class ServiceManager:
    def __init__(self):
        self.services = {}
        self.running = True
        
    def start_service(self, name: str, command: List[str], port: int, 
                     dependencies: List[int] = None, 
                     working_dir: Optional[str] = None) -> bool:
        """Start a service with dependency checking"""
        
        # Check dependencies first
        if dependencies:
            for dep_port in dependencies:
                if not self.wait_for_service(dep_port, timeout=30):
                    print(f"❌ Dependency on port {dep_port} not available for {name}")
                    return False
        
        try:
            # Change working directory if specified
            cwd = working_dir if working_dir else None
            if working_dir:
                os.chdir(working_dir)
            
            print(f"🚀 Starting {name} on port {port}...")
            
            # Start the service
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=cwd
            )
            
            self.services[name] = {
                'process': process,
                'port': port,
                'command': command,
                'working_dir': working_dir
            }
            
            # Wait for service to be ready
            if self.wait_for_service(port, timeout=60):
                print(f"✅ {name} started successfully on port {port}")
                return True
            else:
                print(f"❌ {name} failed to start within timeout")
                self.stop_service(name)
                return False
                
        except Exception as e:
            print(f"❌ Error starting {name}: {e}")
            return False
    
    def wait_for_service(self, port: int, timeout: int = 30) -> bool:
        """Wait for a service to be ready on the specified port"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"http://localhost:{port}/health", timeout=2)
                if response.status_code == 200:
                    return True
            except requests.exceptions.RequestException:
                pass
            
            time.sleep(1)
            
        return False
    
    def stop_service(self, name: str):
        """Stop a specific service"""
        if name in self.services:
            service = self.services[name]
            process = service['process']
            
            try:
                # Terminate gracefully
                process.terminate()
                process.wait(timeout=10)
                print(f"🛑 {name} stopped gracefully")
            except subprocess.TimeoutExpired:
                # Force kill if needed
                process.kill()
                process.wait()
                print(f"🔪 {name} force killed")
            except Exception as e:
                print(f"⚠️ Error stopping {name}: {e}")
            
            del self.services[name]
    
    def stop_all_services(self):
        """Stop all running services"""
        print("\n🛑 Stopping all services...")
        
        # Stop services in reverse order
        service_names = list(self.services.keys())
        for name in reversed(service_names):
            self.stop_service(name)
    
    def check_service_health(self, name: str) -> bool:
        """Check if a service is healthy"""
        if name not in self.services:
            return False
        
        service = self.services[name]
        port = service['port']
        
        try:
            response = requests.get(f"http://localhost:{port}/health", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def monitor_services(self):
        """Monitor service health and restart unhealthy services"""
        while self.running:
            time.sleep(30)  # Check every 30 seconds
            
            for name, service in list(self.services.items()):
                if not self.check_service_health(name):
                    print(f"⚠️ {name} appears unhealthy, attempting restart...")
                    
                    # Stop the unhealthy service
                    self.stop_service(name)
                    
                    # Restart it
                    command = service['command']
                    port = service['port']
                    working_dir = service['working_dir']
                    
                    self.start_service(name, command, port, working_dir=working_dir)


def setup_environment():
    """Setup environment variables and dependencies"""
    print("🔧 Setting up environment...")
    
    # Load .env file
    env_file = backend_dir / ".env"
    if env_file.exists():
        print("📁 Loading environment from .env file")
        
        # Simple .env parser
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Remove quotes if present
                    value = value.strip('"\'')
                    os.environ[key] = value
    
    # Set default values for missing environment variables
    defaults = {
        'MONGODB_URL': 'mongodb://localhost:27017/aura_servicedesk',
        'REDIS_URL': 'redis://localhost:6379',
        'HOST': '0.0.0.0',
        'DEBUG': 'true',
        'LOG_LEVEL': 'INFO'
    }
    
    for key, value in defaults.items():
        if key not in os.environ:
            os.environ[key] = value
            print(f"🔧 Set default {key}={value}")
    
    print("✅ Environment setup complete")


def check_dependencies():
    """Check if required dependencies are available"""
    print("🔍 Checking dependencies...")
    
    dependencies_ok = True
    
    # Check if required Python packages are available
    required_packages = ['fastapi', 'uvicorn', 'pymongo', 'redis', 'openai']
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is available")
        except ImportError:
            print(f"❌ {package} is not installed")
            dependencies_ok = False
    
    # Check if MongoDB is running (optional - service will handle gracefully)
    try:
        import pymongo
        client = pymongo.MongoClient(os.environ.get('MONGODB_URL'), serverSelectionTimeoutMS=2000)
        client.server_info()
        print("✅ MongoDB is available")
    except Exception:
        print("⚠️ MongoDB not available - service will use fallback mode")
    
    # Check if Redis is running (optional - service will handle gracefully)
    try:
        import redis
        client = redis.from_url(os.environ.get('REDIS_URL'), socket_connect_timeout=2)
        client.ping()
        print("✅ Redis is available")
    except Exception:
        print("⚠️ Redis not available - service will use fallback mode")
    
    return dependencies_ok


def main():
    """Main function to start all services robustly"""
    print("🚀 Starting Aura Backend Services (Robust Mode)")
    print("=" * 50)
    
    # Setup
    setup_environment()
    
    if not check_dependencies():
        print("❌ Some dependencies are missing. Please install required packages.")
        print("Run: pip install -r requirements.txt")
        return 1
    
    # Initialize service manager
    manager = ServiceManager()
    
    # Setup signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        print(f"\n📡 Received signal {signum}")
        manager.running = False
        manager.stop_all_services()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start services in dependency order
    services_config = [
        {
            'name': 'Service Desk Host',
            'command': [sys.executable, '-m', 'uvicorn', 'main:app', '--host', '0.0.0.0', '--port', '8001', '--reload'],
            'port': 8001,
            'working_dir': str(backend_dir / 'service-desk-host'),
            'dependencies': []
        },
        {
            'name': 'API Gateway',
            'command': [sys.executable, '-m', 'uvicorn', 'main:app', '--host', '0.0.0.0', '--port', '8000', '--reload'],
            'port': 8000,
            'working_dir': str(backend_dir / 'api-gateway'),
            'dependencies': [8001]  # Depends on Service Desk Host
        }
    ]
    
    # Start services
    all_started = True
    for service_config in services_config:
        success = manager.start_service(
            name=service_config['name'],
            command=service_config['command'],
            port=service_config['port'],
            dependencies=service_config.get('dependencies'),
            working_dir=service_config.get('working_dir')
        )
        
        if not success:
            print(f"❌ Failed to start {service_config['name']}")
            all_started = False
            break
        
        time.sleep(2)  # Give service time to stabilize
    
    if not all_started:
        print("❌ Not all services started successfully")
        manager.stop_all_services()
        return 1
    
    print("\n✅ All services started successfully!")
    print("\n📊 Service Status:")
    print("- API Gateway: http://localhost:8000")
    print("- Service Desk Host: http://localhost:8001")
    print("- API Documentation: http://localhost:8000/docs")
    print("- Health Check: http://localhost:8000/health")
    
    # Start monitoring thread
    monitor_thread = threading.Thread(target=manager.monitor_services, daemon=True)
    monitor_thread.start()
    
    print("\n🔄 Services are running. Press Ctrl+C to stop.")
    
    try:
        # Keep main thread alive
        while manager.running:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        manager.running = False
        manager.stop_all_services()
    
    print("👋 All services stopped. Goodbye!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
