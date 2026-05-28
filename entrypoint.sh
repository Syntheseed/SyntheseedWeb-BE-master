#!/bin/sh
set -e

python manage.py migrate --noinput

exec gunicorn company_backend.wsgi:application \
    --bind 0.0.0.0:80 \
    --workers 3 \
    --timeout 120
