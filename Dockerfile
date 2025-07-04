# Generated by https://smithery.ai. See: https://smithery.ai/docs/build/project-config
FROM python:3.10-slim

# Install dependencies
WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libffi-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml .
COPY src ./src
COPY README.md .

# Install Python dependencies
RUN pip install --no-cache-dir .

# Set default entrypoint
ENTRYPOINT ["amazing-marvin-mcp"]
