# Stage 1: Build environment with dependencies
FROM python:3.9-slim AS builder
WORKDIR /app/aira

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code, configuration, data, and documentation (exclude .env)
COPY aira/ /app/aira/
COPY data/ /app/data/
COPY README.md CODE-OF-CONDUCT.md CONTRIBUTING.md LICENSE SECURITY.md /app/

# Stage 2: Runtime environment
FROM python:3.9-slim
WORKDIR /app/aira

# Copy built dependencies and application from builder
COPY --from=builder /app /app

# Set environment variable for NVIDIA API key (provide at runtime)
ENV NVIDIA_API_KEY=${NVIDIA_API_KEY}

# Expose port for FastAPI/Gradio
EXPOSE 8000

# Run the application
CMD ["python", "app.py"]