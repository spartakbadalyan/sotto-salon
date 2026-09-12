# syntax=docker/dockerfile:1
#
# Backend API image for Sotto Salon (SAL-008).
#
# Build context is the backend/ directory so the lockfile drives a reproducible install:
#   docker build -f infra/Dockerfile -t sotto-salon-api ./backend
#
# The image is traceable by content digest (what the deployment inventory pins), runs as a
# non-root least-privilege user, and carries no secrets — configuration is injected at
# runtime via SALON_* environment variables from the secret manager.

# Reviewed base manifest; update deliberately alongside dependency/security checks.
FROM python:3.12-slim@sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea AS runtime

# No .pyc writing, unbuffered logs, no pip cache or version chatter.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install the exact pinned dependency set first for cache-friendly, reproducible layers,
# then the application itself without re-resolving dependencies.
COPY requirements.lock ./requirements.lock
RUN pip install -r requirements.lock

COPY . .
RUN pip install --no-deps .

# Least privilege: create and drop to a non-root user that does not own the source tree.
RUN useradd --system --create-home --uid 10001 appuser
USER appuser

EXPOSE 8000

# Liveness probe hits the no-secret health endpoint.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health/live', timeout=3).status==200 else 1)"

CMD ["uvicorn", "salon.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
