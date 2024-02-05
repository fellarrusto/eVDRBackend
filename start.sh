#!/bin/sh
# start.sh

echo "Migrations..."
python manage.py migrate --noinput

echo "Starting server..."
gunicorn eVDR.wsgi:application --bind 0.0.0.0:8000
