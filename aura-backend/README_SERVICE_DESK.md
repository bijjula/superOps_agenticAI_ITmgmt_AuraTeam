# Aura Service Desk Host Startup Guide

This guide explains how to start the Aura Service Desk Host on different operating systems. The Service Desk Host requires database services (PostgreSQL, MongoDB, Redis) and proper environment configuration.

## Prerequisites

The Service Desk Host depends on the following services:
- **PostgreSQL** (port 5432) - Main database for structured data
- **MongoDB** (port 27017) - Document storage for tickets and knowledge base
- **Redis** (port 6379) - Caching and session storage
- **OpenAI API Key** - For AI-powered features

## Quick Start

### Option 1: Universal Python Script (Recommended)
Works on **Windows, macOS, and Linux** with automatic dependency checking:
```bash
cd aura-backend
python start_service_desk.py
```

### Option 2: Platform-Specific Scripts

#### For Windows:
```cmd
cd aura-backend
start_service_desk.bat
```

#### For macOS/Linux:
```bash
cd aura-backend
./start_service_desk.sh
```

## Database Setup Instructions

### 🐘 PostgreSQL Setup

#### macOS:
```bash
brew install postgresql
brew services start postgresql
createdb aura_servicedesk
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo -u postgres createdb aura_servicedesk
```

#### Windows:
1. Download from: https://www.postgresql.org/download/windows/
2. Install and create database 'aura_servicedesk' using pgAdmin or psql

### 🍃 MongoDB Setup

#### macOS:
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

#### Linux:
Follow instructions at: https://docs.mongodb.com/manual/installation/
```bash
sudo systemctl start mongod
```

#### Windows:
1. Download from: https://www.mongodb.com/try/download/community
2. Install and start MongoDB service

### 🔴 Redis Setup

#### macOS:
```bash
brew install redis
brew services start redis
```

#### Linux:
```bash
sudo apt-get install redis-server
sudo systemctl start redis-server
```

#### Windows:
1. Download from: https://github.com/microsoftarchive/redis/releases
2. Or use Docker: `docker run -d -p 6379:6379 redis:latest`

## Environment Configuration

### 1. Create .env File
The startup scripts will automatically create a `.env` file from `.env.example` if it doesn't exist.

### 2. Required Environment Variables
Update your `.env` file with these values:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_actual_openai_api_key_here

# Database Configuration
DATABASE_URL=postgresql://aura_user:aura_password@localhost:5432/aura_servicedesk
MONGODB_URL=mongodb://localhost:27017/aura_servicedesk
REDIS_URL=redis://localhost:6379

# Optional Configuration
DEBUG=true
LOG_LEVEL=INFO
```

### 3. Get OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Set `OPENAI_API_KEY` in your `.env` file

## Docker Alternative

If you prefer using Docker for databases:

```bash
# Start all database services with Docker Compose
docker-compose up -d
```

Or start individual services:
```bash
# PostgreSQL
docker run -d --name postgres -p 5432:5432 -e POSTGRES_DB=aura_servicedesk -e POSTGRES_USER=aura_user -e POSTGRES_PASSWORD=aura_password postgres:13

# MongoDB
docker run -d --name mongodb -p 27017:27017 mongo:5

# Redis
docker run -d --name redis -p 6379:6379 redis:latest
```

## What the Scripts Do

All startup methods automatically:
1. ✅ **Check database services** (PostgreSQL, MongoDB, Redis)
2. ✅ **Create .env file** from .env.example if missing
3. ✅ **Validate environment variables**
4. ✅ **Create virtual environment** (if missing)
5. ✅ **Install dependencies** from `requirements.txt`
6. ✅ **Set PYTHONPATH** (fixes import errors)
7. ✅ **Start Service Desk Host** on `http://0.0.0.0:8001`

## Expected Output

When the Service Desk Host starts successfully:
```
🎫 Starting Aura Service Desk Host...
💻 Detected OS: Darwin
✅ .env file already exists
✅ All required environment variables are set
🎫 Checking database services...
✅ PostgreSQL is running on localhost:5432
✅ MongoDB is running on localhost:27017
✅ Redis is running on localhost:6379
✅ Dependencies ready.
🎫 Starting Service Desk Host...
✅ Service Desk Host is starting on http://0.0.0.0:8001
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
```

## API Endpoints

Once running, the Service Desk Host provides:

### Health Check
- **GET** `/health` - Service health status

### Ticket Management
- **POST** `/api/v1/tickets` - Create ticket with AI categorization
- **GET** `/api/v1/tickets` - List tickets with filters
- **GET** `/api/v1/tickets/{id}` - Get specific ticket
- **PUT** `/api/v1/tickets/{id}` - Update ticket
- **POST** `/api/v1/tickets/{id}/categorize` - Re-categorize with AI

### Knowledge Base
- **POST** `/api/v1/kb/articles` - Create KB article
- **GET** `/api/v1/kb/articles` - List KB articles
- **GET** `/api/v1/kb/articles/{id}` - Get specific article
- **POST** `/api/v1/kb/search` - AI-powered KB search

### Chatbot
- **POST** `/api/v1/chatbot/message` - Process chatbot message

### Documentation
- **Interactive API Docs**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

## Troubleshooting

### Database Connection Errors
```
❌ PostgreSQL is not running on localhost:5432
```
**Solution**: Start PostgreSQL service using the setup instructions above.

### Missing Environment Variables
```
❌ Missing required environment variables: OPENAI_API_KEY
```
**Solution**: Update your `.env` file with the missing values.

### Import Errors
```
ModuleNotFoundError: No module named 'shared'
```
**Solution**: This is automatically fixed by setting `PYTHONPATH=.` which all scripts do.

### OpenAI API Errors
```
OpenAI API error: Invalid API key
```
**Solution**: 
1. Verify your OpenAI API key is correct
2. Check you have credits in your OpenAI account
3. Ensure the key has proper permissions

### Port Already in Use
```
Address already in use: port 8001
```
**Solution**: Either stop the existing service or change the port in your environment:
```env
PORT=8002
```

## Features

The Service Desk Host includes:

### 🤖 AI-Powered Features
- **Automatic ticket categorization** using OpenAI
- **Intelligent knowledge base search**
- **AI chatbot** for self-service support
- **KB article recommendations** based on ticket content

### 🎫 Ticket Management
- Create, read, update tickets
- Filter by status, category, assignee
- File attachments support
- Priority management

### 📚 Knowledge Base
- Article creation and management
- Full-text search capabilities
- Category organization
- Usage analytics (views, votes)

### 💬 Chatbot Integration
- Natural language processing
- Context-aware responses
- Escalation to human agents
- Integration with knowledge base

## Development Mode

To run in development mode with auto-reload:
```bash
# Set DEBUG=true in .env file
DEBUG=true

# The service will auto-reload on code changes
```

## Stopping the Service

Press `Ctrl+C` in the terminal to stop the Service Desk Host.

## Next Steps

1. Start the API Gateway: `python start_api_gateway.py`
2. Start the frontend application
3. Test the integration between services
4. Configure additional AI features as needed
