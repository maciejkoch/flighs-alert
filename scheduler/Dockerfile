# Scheduler service Dockerfile
FROM python:3.13-slim

# Install uv
RUN pip install uv

# Set workdir
WORKDIR /app

# Copy dependency files from parent directory
COPY pyproject.toml uv.lock ./

# Install dependencies (cached if no changes)
RUN uv sync --frozen --no-dev

# Copy entire application (needed for imports)
COPY . .

# Make scheduler script executable
RUN chmod +x /app/scheduler/flights

# Run the flights scheduler script
CMD ["uv", "run", "python", "/app/scheduler/flights"]
