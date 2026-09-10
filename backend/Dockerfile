# syntax=docker/dockerfile:1

FROM python:3.12-slim

WORKDIR /app

# Python runtime configuration
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create a non-root application user
RUN addgroup --system app && \
    adduser --system --ingroup app app

# Install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY --chown=app:app app/ ./app/

# Run as non-root user
USER app

EXPOSE 8000

# Container health check
HEALTHCHECK --interval=30s \
            --timeout=5s \
            --start-period=10s \
            --retries=3 \
            CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health')" || exit 1

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]