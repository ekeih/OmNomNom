#! /usr/bin/env sh

case "$1" in
  "beat")
    python3 warmup_cache.py
    exec celery -A backend.backend beat -l info
    ;;
  "flower")
    exec celery flower -A backend.backend --address=0.0.0.0 --broker="redis://${OMNOMNOM_REDIS_HOST}:6379/1"
    ;;
  "frontend")
    exec python3 frontend/frontend.py
    ;;
  "worker")
    exec celery -A backend.backend worker -l info -Q canteens
    ;;
  "housekeeping")
    exec celery -A backend.backend worker -l info -Q housekeeping
    ;;
  *)
    echo "You need to pass beat, frontend, housekeeping or worker as an argument!" >&2
    exit 1
    ;;
esac
