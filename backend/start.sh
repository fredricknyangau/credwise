#!/bin/bash
set -e

echo "Running migrations..."
alembic upgrade head

echo "Running seed script..."
python scripts/seed.py

echo "Starting Uvicorn..."
# Render provides the $PORT environment variable
PORT="${PORT:-8000}"
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
