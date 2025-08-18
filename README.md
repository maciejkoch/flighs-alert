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
