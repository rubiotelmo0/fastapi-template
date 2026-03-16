#!/bin/bash
set -euo pipefail

terminate() {
  echo "Termination signal received, shutting down..."
  if [[ -n "${HYPERCORN_PID:-}" ]]; then
    kill -SIGTERM "$HYPERCORN_PID"
    wait "$HYPERCORN_PID"
  fi
  echo "Hypercorn has been terminated"
}

trap terminate SIGTERM SIGINT

APP_MODULE="${APP_MODULE:-app.main:app}"
PORT="${PORT:-8000}"

hypercorn \
  --bind "0.0.0.0:${PORT}" \
  "${APP_MODULE}" &

HYPERCORN_PID=$!
wait "$HYPERCORN_PID"
