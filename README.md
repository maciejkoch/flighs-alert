# Flights Alert - Microservices Architecture

A service for monitoring flight prices and receiving alerts on price drops, built with a microservices architecture.

## 🏗️ Architecture Overview

```
flights-alert/
├── shared/                     # Shared library
│   ├── models/                 # Pydantic models (Flight)
│   └── services/              # Business logic (FlightsService)
├── services/
│   ├── api/                   # FastAPI service
│   │   ├── pyproject.toml     # API-specific dependencies
│   │   ├── Dockerfile         # API service container
│   │   └── main.py           # FastAPI application
│   └── scheduler/             # Scheduler service
│       ├── pyproject.toml     # Minimal scheduler dependencies
│       ├── Dockerfile         # Scheduler service container
│       └── flights           # Executable scheduler script
└── response-examples/         # Example responses
```

## 🎯 Services

### 📡 API Service (`services/api/`)

- **Purpose**: REST API for flight data
- **Dependencies**: FastAPI, Uvicorn, Requests, BeautifulSoup4, Pydantic
- **Port**: 8000
- **Endpoints**:
  - `GET /` - Returns flight search results
  - `GET /health` - Health check

### ⏰ Scheduler Service (`services/scheduler/`)

- **Purpose**: Automated flight monitoring jobs
- **Dependencies**: Requests, BeautifulSoup4, Pydantic (minimal set)
- **Execution**: Prints "Job is working" and can fetch flight data

### 📚 Shared Library (`shared/`)

- **Models**: Flight data structures (Pydantic models)
- **Services**: FlightsService for web scraping and data parsing
- **Used by**: Both API and Scheduler services

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

Each service has its own Dockerfile with optimized dependencies:

### Build API Service

```bash
docker build -f Dockerfile.api -t flights-api .
docker run -p 8000:8000 flights-api
```

### Build Scheduler Service

```bash
docker build -f Dockerfile.scheduler -t flights-scheduler .
docker run flights-scheduler
```

## ☁️ Railway Deployment

### Option 1: Separate Services (Recommended)

**API Service:**

1. Create Railway service from repo
2. Set build source: `Dockerfile.api`
3. Service will run on assigned port

**Scheduler Service:**

1. Create second Railway service from same repo
2. Set build source: `Dockerfile.scheduler`
3. Service runs scheduler job once and exits (perfect for cron)

### Option 2: Cron Jobs

Deploy API service normally, then add cron jobs:

```bash
# In Railway cron tab
uv run python services/scheduler/flights
```

## 🔧 Benefits of This Architecture

### ✅ **Separation of Concerns**

- API handles HTTP requests
- Scheduler handles background jobs
- Shared library prevents code duplication

### ✅ **Independent Scaling**

- Scale API service based on traffic
- Run scheduler service on schedule
- Different resource requirements

### ✅ **Optimized Dependencies**

- API service: Full web stack (FastAPI, Uvicorn)
- Scheduler: Minimal deps (no web server needed)
- Shared: Core business logic only

### ✅ **Independent Deployment**

- Deploy API without affecting scheduler
- Deploy scheduler without affecting API
- Each service has its own build context

### ✅ **Development Flexibility**

- Work on services independently
- Test services in isolation
- Different teams can own different services

## 🛠️ Development

### Adding New Features

1. **Shared logic** → Add to `shared/services/` or `shared/models/`
2. **API endpoints** → Add to `services/api/api/`
3. **Scheduled tasks** → Extend `services/scheduler/flights`

### Testing

Each service can be tested independently:

```bash
# Test API
cd services/api && uv run python -m pytest

# Test Scheduler
cd services/scheduler && uv run python flights
```

This microservices architecture provides flexibility, maintainability, and optimal resource usage for your flights alert system!
