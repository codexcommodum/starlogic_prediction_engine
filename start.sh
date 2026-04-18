#!/bin/sh
# Startup script — handles PORT from env var with fallback
PORT="${PORT:-8000}"
echo "Starting uvicorn on port $PORT"
exec uvicorn main:app --host 0.0.0.0 --port "$PORT"
