#!/bin/bash

# Fly.io Deployment Script for JWT Authentication API

echo "JWT Authentication API - Fly.io Deployment"
echo "==========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if flyctl is installed
if ! command -v flyctl &> /dev/null; then
    print_error "flyctl is not installed. Please install it first:"
    echo "curl -L https://fly.io/install.sh | sh"
    exit 1
fi

# Check if user is logged in
if ! flyctl auth whoami &> /dev/null; then
    print_warning "Please log in to Fly.io first:"
    echo "flyctl auth login"
    exit 1
fi

print_status "Deploying JWT Authentication API to Fly.io..."

# Create app if it doesn't exist
print_status "Creating/updating Fly.io app..."
flyctl apps create jwt-auth-api --org personal || print_warning "App might already exist"

# Set secrets
print_status "Setting environment secrets..."
echo "Please set the following secrets (press Enter to skip if already set):"

read -p "Enter your Django SECRET_KEY (or press Enter to generate): " SECRET_KEY
if [ -z "$SECRET_KEY" ]; then
    SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
fi

read -p "Enter your JWT_SECRET_KEY (or press Enter to generate): " JWT_SECRET_KEY
if [ -z "$JWT_SECRET_KEY" ]; then
    JWT_SECRET_KEY=$(openssl rand -base64 32)
fi

flyctl secrets set SECRET_KEY="$SECRET_KEY" JWT_SECRET_KEY="$JWT_SECRET_KEY" --app jwt-auth-api

# Deploy the app
print_status "Deploying application..."
flyctl deploy --app jwt-auth-api

# Create sample users
print_status "Creating sample users..."
flyctl ssh console --app jwt-auth-api --command "python manage.py create_sample_users"

# Get app URL
APP_URL=$(flyctl info --app jwt-auth-api | grep "Hostname" | awk '{print $2}')

print_status "Deployment completed successfully!"
echo ""
echo "Your JWT Authentication API is now live at:"
echo "https://${APP_URL}"
echo ""
echo "API Endpoints:"
echo "- POST https://${APP_URL}/api/auth/register/"
echo "- POST https://${APP_URL}/api/auth/login/"
echo "- POST https://${APP_URL}/api/auth/verify/"
echo "- GET https://${APP_URL}/api/auth/validate/"
echo "- GET https://${APP_URL}/swagger/"
echo "- GET https://${APP_URL}/redoc/"
echo ""
echo "Sample credentials:"
echo "- admin / admin123"
echo "- testuser / testpass123"
echo "- demo / demo123"
echo ""
print_status "Deployment completed successfully! 🎉"
