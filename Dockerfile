# Use recommended secure base image (Python 3.13 on Bookworm)
FROM python:3.13-slim-bookworm

# Set security-hardened environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PATH="/home/appuser/.local/bin:$PATH"

# Install system dependencies with security best practices
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    # Clean up aggressively
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m appuser

WORKDIR /app

# Switch to non-root user early
USER appuser

# Install Python dependencies securely
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy application files
COPY --chown=appuser:appuser . .

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import requests; requests.get('http://localhost:5000/health', timeout=5) or exit(1)"

# Run the application
CMD ["python", "app.py"]
