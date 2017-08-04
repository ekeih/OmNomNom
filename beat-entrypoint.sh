#! /bin/sh

rm /app/celerybeat.pid
exec celery -A backend.backend beat -l info