#!/bin/bash
set -e  # Terminate the script on error

echo "Waiting for database..."
sleep 5  # Allow time for the database to run

echo "Applying migrations..."
alembic upgrade head

echo "Starting application..."
exec gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
