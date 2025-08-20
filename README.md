# Flights Alert - Independent Services

A simple microservices project with independent API and Scheduler services.

## 🏗️ Architecture Overview

```
flights-alert/
├── services/
│   ├── api/                   # Simple FastAPI service
│   │   ├── Dockerfile         # API service container
│   │   ├── pyproject.toml     # Minimal dependencies (FastAPI, Uvicorn)
│   │   └── main.py           # Returns "Hello world"
│   └── scheduler/             # Flights monitoring service  
│       ├── Dockerfile         # Scheduler service container
│       ├── pyproject.toml     # Full flight monitoring dependencies
│       ├── flights           # Executable scheduler script
│       ├── models/           # Flight data models
│       └── services/         # Flight monitoring logic
└── response-examples/         # Example responses
```

## 🎯 Services

### 📡 API Service (`services/api/`)
- **Purpose**: Simple REST API 
- **Dependencies**: FastAPI, Uvicorn only
- **Endpoints**:
  - `GET /` - Returns `"Hello world"`
  - `GET /health` - Returns `{"status": "ok"}`

### ⏰ Scheduler Service (`services/scheduler/`)
- **Purpose**: Flight price monitoring and alerts
- **Dependencies**: Requests, BeautifulSoup4, Pydantic
- **Execution**: Prints "Job is working" and monitors flight data
- **Contains**: All flight monitoring logic, models, and services

## 🚀 Running Services

### API Service
```bash
cd services/api
uv run python main.py
```
Access at: http://localhost:8000

### Scheduler Service
```bash
cd services/scheduler
uv run python flights
```

## 🐳 Docker Deployment

Each service has its own Dockerfile in its directory:

### Build API Service
```bash
cd services/api
docker build -t flights-api .
docker run -p 8000:8000 flights-api
```

### Build Scheduler Service  
```bash
cd services/scheduler
docker build -t flights-scheduler .
docker run flights-scheduler
```

## ☁️ Railway Deployment

### 🎯 **Easy Setup - Each Service Deployed Separately**

**API Service:**
1. Create Railway service from GitHub repo
2. **Source**: `services/api` directory
3. **Dockerfile**: Auto-detected (`services/api/Dockerfile`)
4. Railway will run: `uvicorn main:app --host 0.0.0.0 --port 8000`

**Scheduler Service:**
1. Create second Railway service from same GitHub repo  
2. **Source**: `services/scheduler` directory
3. **Dockerfile**: Auto-detected (`services/scheduler/Dockerfile`)
4. Railway will run the scheduler once and exit

### 📋 **Railway Configuration**

**API Service Settings:**
```
Repository: your-username/flights-alert
Root Directory: services/api
Build: Auto-detected Dockerfile
```

**Scheduler Service Settings:**
```
Repository: your-username/flights-alert
Root Directory: services/scheduler  
Build: Auto-detected Dockerfile
```

### 🔄 **For Scheduled Jobs**

**Option 1: Railway Cron**
- Deploy scheduler service as above
- In Railway: Add cron job pointing to scheduler service
- Schedule: `0 */6 * * *` (every 6 hours)

**Option 2: Restart Policy**
- Set scheduler service to restart periodically
- Perfect for regular flight monitoring

## 🔧 Benefits of This Architecture

### ✅ **True Independence**
- **API**: Ultra-lightweight, only web dependencies
- **Scheduler**: Complete flight monitoring system
- **No shared code**: Each service is self-contained

### ✅ **Simple Railway Deployment**
- **No custom build configurations needed**
- **Each service deployed from its own directory**
- **Railway auto-detects everything**

### ✅ **Optimized for Purpose**
- **API**: Fast startup, minimal resources
- **Scheduler**: Full business logic, runs when needed
- **Different scaling patterns**

### ✅ **Easy Development**
- **Work on services independently**
- **Test in isolation**
- **Deploy independently**

## 🛠️ Development

### Adding API Features
1. Edit `services/api/main.py`
2. Add dependencies to `services/api/pyproject.toml`
3. Test with `uv run python main.py`

### Extending Scheduler
1. Modify `services/scheduler/flights`
2. Add models in `services/scheduler/models/`
3. Extend services in `services/scheduler/services/`
4. Test with `uv run python flights`

## 🎉 Railway Deployment Steps

1. **Push code to GitHub**
2. **Deploy API Service**:
   - New Railway project from GitHub
   - Root directory: `services/api`
   - Deploy automatically
3. **Deploy Scheduler Service**:
   - Add service to same Railway project
   - Root directory: `services/scheduler`
   - Deploy automatically
4. **Set up scheduling** (optional):
   - Add cron job in Railway dashboard
   - Point to scheduler service

**Both services will work perfectly with Railway's auto-detection!** 🚀