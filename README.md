# 🌟 Aura - AI-Powered IT Management Suite

A comprehensive IT service management platform built with **Python FastAPI microservices** backend and **React.js** frontend, featuring AI-powered ticket routing, knowledge base optimization, and intelligent chatbot assistance.

## 📋 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [🏗️ Project Structure](#️-project-structure)
- [🔧 Prerequisites](#-prerequisites)
- [⚙️ Installation & Setup](#️-installation--setup)
- [🏃‍♂️ Running the Application](#️-running-the-application)
- [🧪 Testing](#-testing)
- [🔍 Troubleshooting](#-troubleshooting)
- [📚 API Documentation](#-api-documentation)
- [🎨 UI/UX Features](#-uiux-features)
- [🤝 Contributing](#-contributing)

## 🚀 Quick Start

**For impatient developers - get running in 5 minutes:**

```bash
# 1. Clone the repository
git clone https://github.com/bijjula/superOps_vibecoding.git
cd superOps_vibecoding

# 2. Backend Setup (Terminal 1)
cd aura-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r api-gateway/requirements.txt
pip install -r service-desk-host/requirements.txt
python api-gateway/main.py

# 3. Frontend Setup (Terminal 2)
cd aura-frontend
npm install
npm start

# 4. Open http://localhost:3000 in your browser
```

## 🏗️ Project Structure

```
superOps_vibecoding/
├── 📂 aura-backend/              # Python FastAPI Microservices
│   ├── 📂 api-gateway/           # Main API Gateway
│   │   ├── main.py               # Gateway entry point
│   │   ├── requirements.txt      # Python dependencies
│   │   └── Dockerfile           # Container config
│   ├── 📂 service-desk-host/     # Service Desk Microservice
│   │   ├── main.py               # Service entry point
│   │   ├── requirements.txt      # Service dependencies
│   │   └── Dockerfile           # Container config
│   ├── 📂 shared/               # Shared utilities
│   │   ├── 📂 database/         # Database utilities
│   │   ├── 📂 middleware/       # Common middleware
│   │   ├── 📂 models/           # Shared data models
│   │   └── 📂 utils/            # AI services & utilities
│   ├── .env.example             # Environment variables template
│   └── docker-compose.yml       # Multi-service orchestration
├── 📂 aura-frontend/            # React.js Frontend Application
│   ├── 📂 public/               # Static assets
│   ├── 📂 src/                  # Source code
│   │   ├── 📂 components/       # Reusable UI components
│   │   │   └── 📂 layout/       # Layout components (Header, Sidebar)
│   │   ├── 📂 pages/            # Application pages
│   │   │   ├── 📂 Dashboard/    # Main dashboard
│   │   │   ├── 📂 ServiceDesk/  # Ticket management
│   │   │   ├── 📂 KnowledgeBase/# Knowledge base interface
│   │   │   └── 📂 Chatbot/      # AI assistant interface
│   │   ├── 📂 services/         # API service layer
│   │   ├── 📂 theme/            # SAP Fiori theme configuration
│   │   ├── App.js               # Main app component
│   │   └── index.js             # Entry point
│   ├── package.json             # Node.js dependencies
│   └── package-lock.json        # Dependency lock file
├── 📂 docs/                     # Project documentation
│   ├── Functional_Specification_Document.md
│   └── Product_Requirement_Document.md
├── 📂 prompts/                  # Development prompts & guides
└── README.md                    # This file
```

## 🔧 Prerequisites

Ensure you have the following installed on your system:

### Required Software

| Software | Version | Installation |
|----------|---------|--------------|
| **Python** | 3.8+ | [Download Python](https://python.org/downloads/) |
| **Node.js** | 16+ | [Download Node.js](https://nodejs.org/) |
| **npm** | 8+ | Comes with Node.js |
| **Git** | Latest | [Download Git](https://git-scm.com/) |

### Optional (for containers)
- **Docker** 20.10+ - [Download Docker](https://docker.com/get-started)
- **Docker Compose** 2.0+ - Usually included with Docker Desktop

### Verify Installation

```bash
# Check versions
python --version    # Should show Python 3.8+
node --version      # Should show Node v16+
npm --version       # Should show npm 8+
git --version       # Should show git version
```

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/bijjula/superOps_vibecoding.git
cd superOps_vibecoding
```

### 2. Backend Setup (Python FastAPI Microservices)

```bash
# Navigate to backend directory
cd aura-backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r api-gateway/requirements.txt
pip install -r service-desk-host/requirements.txt

# Optional: Set up environment variables
cp .env.example .env
# Edit .env file with your configuration
```

### 3. Frontend Setup (React.js Application)

```bash
# Navigate to frontend directory (in a new terminal)
cd aura-frontend

# Install Node.js dependencies
npm install

# Optional: Verify installation
npm list --depth=0
```

## 🏃‍♂️ Running the Application

### Development Mode (Recommended)

**Option 1: Manual Start (2 terminals)**

```bash
# Terminal 1 - Backend API Gateway
cd aura-backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python api-gateway/main.py

# Terminal 2 - Frontend Development Server
cd aura-frontend
npm start
```

**Option 2: Using Docker Compose**

```bash
# From project root
cd aura-backend
docker-compose up --build
```

### Access the Application

- **Frontend Application**: http://localhost:3000
- **API Gateway**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Swagger UI)

### Default Ports

| Service | Port | URL |
|---------|------|-----|
| React Frontend | 3000 | http://localhost:3000 |
| API Gateway | 8000 | http://localhost:8000 |
| Service Desk API | 8001 | http://localhost:8001 |
| Swagger Docs | 8000 | http://localhost:8000/docs |

## 🧪 Testing

### Frontend Testing

```bash
cd aura-frontend

# Run tests
npm test

# Run tests in watch mode
npm test -- --watch

# Generate coverage report
npm test -- --coverage
```

### Backend Testing

```bash
cd aura-backend
source venv/bin/activate

# Run API tests
python -m pytest

# Run with coverage
python -m pytest --cov=. --cov-report=html
```

### Manual Testing

1. **Frontend**: Navigate to http://localhost:3000
2. **API Health**: Check http://localhost:8000/health
3. **Documentation**: Browse http://localhost:8000/docs

## 🔍 Troubleshooting

### Common Issues & Solutions

#### ❌ **Port Already in Use**
```bash
# Kill process on port 3000 (React)
lsof -ti:3000 | xargs kill -9

# Kill process on port 8000 (API)
lsof -ti:8000 | xargs kill -9
```

#### ❌ **Python Virtual Environment Issues**
```bash
# Remove existing venv and recreate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r api-gateway/requirements.txt
```

#### ❌ **Node Modules Issues**
```bash
# Clear npm cache and reinstall
cd aura-frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

#### ❌ **CORS Issues**
- Backend API Gateway already configured for CORS
- Frontend runs on port 3000, backend on 8000
- Check browser developer tools for specific CORS errors

#### ❌ **Module Import Errors**
```bash
# Backend: Check Python path
cd aura-backend
export PYTHONPATH=$PWD:$PYTHONPATH
python api-gateway/main.py

# Frontend: Clear React cache
cd aura-frontend
npm start -- --reset-cache
```

### Environment-Specific Issues

#### macOS
```bash
# If you get SSL certificate errors
pip install --upgrade certifi
```

#### Windows
```bash
# Use PowerShell or Command Prompt
# Activate virtual environment
venv\Scripts\activate.bat
```

#### Linux
```bash
# Install additional dependencies if needed
sudo apt-get update
sudo apt-get install python3-venv python3-dev
```

### Getting Help

1. **Check Logs**: Both terminals will show error messages
2. **Browser DevTools**: Press F12 to see frontend errors
3. **API Documentation**: Visit http://localhost:8000/docs for API details
4. **GitHub Issues**: Report bugs or ask questions in the repository

## 📚 API Documentation

### Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/tickets` | GET, POST | Ticket management |
| `/api/tickets/{id}` | GET, PUT, DELETE | Individual ticket operations |
| `/api/knowledge-base` | GET | Search knowledge base |
| `/api/chat` | POST | AI chatbot interaction |

### Example API Usage

```bash
# Health check
curl http://localhost:8000/health

# Get all tickets
curl http://localhost:8000/api/tickets

# Create a ticket
curl -X POST http://localhost:8000/api/tickets \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Issue", "description": "Sample ticket"}'
```

## 🎨 UI/UX Features

### Frontend Highlights

- **🎨 SAP Fiori Theme**: Professional enterprise design
- **📱 Responsive Design**: Works on desktop, tablet, and mobile
- **🔍 Interactive Dashboard**: Real-time metrics and charts
- **🎫 Ticket Management**: Create, view, and manage support tickets
- **📚 Knowledge Base**: Searchable articles and documentation
- **🤖 AI Chatbot**: Intelligent assistance for common issues
- **🧭 Intuitive Navigation**: Clean sidebar with clear menu structure

### Key Pages

1. **Dashboard** (`/dashboard`) - Overview of IT operations
2. **Service Desk** (`/tickets`) - Ticket management interface
3. **Knowledge Base** (`/knowledge-base`) - Searchable help articles
4. **AI Chatbot** (`/chatbot`) - Interactive assistance

## 🤝 Contributing

### Development Workflow

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Make** your changes
4. **Test** thoroughly (frontend + backend)
5. **Commit** your changes: `git commit -m 'Add amazing feature'`
6. **Push** to branch: `git push origin feature/amazing-feature`
7. **Open** a Pull Request

### Code Style

- **Backend**: Follow PEP 8 (Python)
- **Frontend**: Use ESLint and Prettier
- **Commits**: Use conventional commit messages

### Running Code Quality Checks

```bash
# Backend linting
cd aura-backend
flake8 .

# Frontend linting
cd aura-frontend
npm run lint
npm run lint:fix
```

---

## 📞 Support

If you encounter any issues or need assistance:

1. **Check this README** for common solutions
2. **Review the troubleshooting section** above
3. **Open an issue** on GitHub with detailed information
4. **Include logs** from both frontend and backend when reporting issues

---

**🚀 Happy Coding! Welcome to the Aura AI-Powered IT Management Suite!**
