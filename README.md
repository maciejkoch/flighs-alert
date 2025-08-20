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

The project includes a scheduler script for Railway's cron jobs:

### Running the scheduler locally

```bash
uv run scheduler.py
```

### Deploying to Railway

1. Deploy your application to Railway
2. In your Railway project dashboard, go to the "Cron" tab
3. Add a new cron job with the command: `uv run scheduler.py`
4. Set your desired schedule (e.g., `0 */6 * * *` for every 6 hours)

The scheduler script will output:

- "Job is working"
- Current timestamp
- Success confirmation
