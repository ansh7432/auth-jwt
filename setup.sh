#!/bin/bash

# Setup script for JWT Authentication API

echo "Setting up JWT Authentication API..."

# Activate virtual environment
source venv/bin/activate

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional, for admin access)
echo "Creating superuser..."
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else print('Admin user already exists')" | python manage.py shell

# Create sample users
echo "Creating sample users..."
python manage.py create_sample_users

echo "Setup completed successfully!"
echo ""
echo "Sample credentials:"
echo "- admin / admin123"
echo "- testuser / testpass123"
echo "- demo / demo123"
echo ""
echo "To start the server, run:"
echo "python manage.py runserver"
