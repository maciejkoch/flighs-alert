# Use official Python base
FROM python:3.13-slim

# Install uv
RUN pip install uv

# Set workdir
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies (cached if no changes)
RUN uv sync --frozen --no-dev

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run app with uvicorn (Railway will set PORT env variable)
CMD uv run uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
