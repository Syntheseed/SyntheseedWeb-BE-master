# ---------- Build stage ----------
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Runtime stage ----------
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy Django project (frontend files excluded via .dockerignore)
COPY . .

# Create dirs for static/media
RUN mkdir -p /app/staticfiles /app/media

ENV DJANGO_SETTINGS_MODULE=company_backend.settings
ENV PYTHONUNBUFFERED=1

# Collect static files at build time
RUN python manage.py collectstatic --noinput 2>/dev/null || true

EXPOSE 80

USER root

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
