# Scheduler service Dockerfile
FROM python:3.13-slim

# Install uv
RUN pip install uv

# Set workdir
WORKDIR /app

# Copy dependency files for this service
COPY services/scheduler/pyproject.toml ./

# Generate lock file and install dependencies
RUN uv lock && uv sync --frozen --no-dev

# Copy shared library
COPY shared/ ./shared/

# Copy scheduler service code
COPY services/scheduler/ ./

# Make scheduler script executable
RUN chmod +x /app/flights

# Run the scheduler script
CMD ["uv", "run", "python", "/app/flights"]
