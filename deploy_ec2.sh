#!/bin/bash

# AWS EC2 Deployment Script for JWT Authentication API

echo "JWT Authentication API - AWS EC2 Deployment"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

# Update system
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Docker if not present
if ! command -v docker &> /dev/null; then
    print_status "Installing Docker..."
    sudo apt install -y docker.io
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker $USER
    print_warning "Please log out and log back in for Docker permissions to take effect"
else
    print_status "Docker already installed"
fi

# Install Docker Compose if not present
if ! command -v docker-compose &> /dev/null; then
    print_status "Installing Docker Compose..."
    sudo apt install -y docker-compose
else
    print_status "Docker Compose already installed"
fi

# Install Git if not present
if ! command -v git &> /dev/null; then
    print_status "Installing Git..."
    sudo apt install -y git
else
    print_status "Git already installed"
fi

# Clone repository (adjust URL as needed)
print_status "Cloning repository..."
if [ -d "jwt-auth-api" ]; then
    print_warning "Directory jwt-auth-api already exists, pulling latest changes..."
    cd jwt-auth-api
    git pull
else
    # Replace with your actual repository URL
    print_warning "Replace <YOUR_REPO_URL> with your actual repository URL"
    # git clone <YOUR_REPO_URL> jwt-auth-api
    # cd jwt-auth-api
fi

# Configure environment variables
print_status "Configuring environment variables..."
echo "Please update the following environment variables in docker-compose.yml:"
echo "- SECRET_KEY (Django secret key)"
echo "- JWT_SECRET_KEY (JWT signing key)"
echo "- ALLOWED_HOSTS (your domain/IP)"
echo ""
echo "Example:"
echo "  environment:"
echo "    - DEBUG=False"
echo "    - SECRET_KEY=your-very-secure-secret-key-here"
echo "    - JWT_SECRET_KEY=your-jwt-secret-key-here"
echo "    - ALLOWED_HOSTS=yourdomain.com,your-ec2-public-ip"
echo ""
read -p "Press enter to continue after updating docker-compose.yml..."

# Build and run with Docker Compose
print_status "Building and starting containers..."
docker-compose up -d --build

# Wait for containers to be ready
print_status "Waiting for containers to be ready..."
sleep 10

# Run database migrations
print_status "Running database migrations..."
docker-compose exec web python manage.py migrate

# Create sample users
print_status "Creating sample users..."
docker-compose exec web python manage.py create_sample_users

# Configure firewall (UFW)
print_status "Configuring firewall..."
sudo ufw allow 8000/tcp
sudo ufw --force enable

# Display final information
print_status "Deployment completed successfully!"
echo ""
echo "Your JWT Authentication API is now running on:"
echo "- Local: http://localhost:8000/api/auth/"
echo "- Public: http://$(curl -s ifconfig.me):8000/api/auth/"
echo ""
echo "Sample credentials:"
echo "- admin / admin123"
echo "- testuser / testpass123"
echo "- demo / demo123"
echo ""
echo "API Endpoints:"
echo "- POST /api/auth/login/"
echo "- POST /api/auth/verify/"
echo "- GET /api/auth/validate/"
echo ""
echo "To check logs: docker-compose logs -f"
echo "To stop: docker-compose down"
echo "To restart: docker-compose restart"
echo ""
print_status "Deployment completed successfully! 🎉"
