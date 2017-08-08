#! /usr/bin/env sh

case "$1" in
  "beat")
    python3 warmup_cache.py
    exec celery -A backend.backend beat -l info
    ;;
  "frontend")
    exec python3 frontend.py
    ;;
  "worker")
    exec celery -A backend.backend worker -l info
    ;;
  *)
    echo "You need to pass beat, frontend or worker as an argument!" >&2
    exit 1
    ;;
esac
