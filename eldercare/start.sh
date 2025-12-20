#!/bin/bash

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
while ! pg_isready -h 127.0.0.1 -p 5432 -U postgres; do
  sleep 1
done
echo "PostgreSQL is ready!"

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Start Django server
python manage.py runserver 0.0.0.0:8000
