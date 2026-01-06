#!/bin/bash
set -e

# optional: run migrations, collectstatic
python manage.py migrate --noinput
# If you serve static from container (not recommended for production CDN):
python manage.py collectstatic --noinput

# Start Uvicorn
exec python manage.py runserver 0.0.0.0:8000
 