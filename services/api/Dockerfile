# Simple API service Dockerfile
FROM python:3.13-slim

# Install uv
RUN pip install uv

# Set workdir
WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./

# Generate lock file and install dependencies
RUN uv lock && uv sync --frozen --no-dev

# Copy API service code
COPY . .

# Expose port
EXPOSE 8000

# Run the API service
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
