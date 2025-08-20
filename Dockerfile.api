# API service Dockerfile
FROM python:3.13-slim

# Install uv
RUN pip install uv

# Set workdir
WORKDIR /app

# Copy dependency files for this service
COPY services/api/pyproject.toml ./

# Generate lock file and install dependencies
RUN uv lock && uv sync --frozen --no-dev

# Copy shared library
COPY shared/ ./shared/

# Copy API service code
COPY services/api/ ./

# Expose port
EXPOSE 8000

# Run the API service
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
