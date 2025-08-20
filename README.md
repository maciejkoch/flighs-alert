# Flights Alert

A service for monitoring flight prices and receiving alerts on price drops.

## Setup

This project uses Python 3.13 and [uv](https://github.com/astral-sh/uv) for dependency management.

Dependencies are automatically installed when you run the application with uv.

## Running the API

You can run the API in two ways:

### Using the start script

```bash
uv run start.py
```

### Directly with Python

```bash
uv run dev.py
```

The API will be available at [http://localhost:8000](http://localhost:8000)

## Available Endpoints

- `GET /` - Returns "hello world"
- `GET /health` - Returns API health status

## Scheduler

The project includes a dedicated scheduler service for flight monitoring:

### Running the scheduler locally

```bash
uv run python scheduler/flights
```

### Deploying to Railway

**Option 1: Separate Service (Recommended)**

1. Create a new Railway service from the same repository
2. Set the build source to use `scheduler/Dockerfile`
3. The service will automatically run the flights monitoring job

**Option 2: Cron Job on Main Service**

1. Deploy your main FastAPI application to Railway
2. In your Railway project dashboard, go to the "Cron" tab
3. Add a new cron job with the command: `uv run python scheduler/flights`
4. Set your desired schedule (e.g., `0 */6 * * *` for every 6 hours)

### Scheduler Structure

```
scheduler/
├── Dockerfile      # Docker configuration for scheduler service
└── flights         # Executable Python script for flight monitoring
```

The scheduler will:

- Import and use your existing flight services
- Output detailed logging with timestamps
- Handle errors gracefully
- Execute flight monitoring tasks
