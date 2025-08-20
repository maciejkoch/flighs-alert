# Scheduler service Dockerfile
FROM python:3.13-slim

# Install uv
RUN pip install uv

# Set workdir
WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./

# Generate lock file and install dependencies
RUN uv lock && uv sync --frozen --no-dev

# Copy scheduler service code
COPY . .

# Make scheduler script executable
RUN chmod +x /app/flights-scheduler.py

# Run the scheduler script
CMD ["uv", "run", "python", "/app/flights-scheduler.py"]
