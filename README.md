# JWT Authentication API

A Django REST Framework-based JWT authentication API with Docker support, designed for deployment on AWS EC2.

## Features

- JWT-based authentication
- Three main endpoints: login, verify, and validate
- Docker containerization
- AWS EC2 deployment ready
- Sample user credentials included

## API Endpoints

### 1. User Registration
- **POST** `/api/auth/register/`
- **Request Body:**
  ```json
  {
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "first_name": "New",
    "last_name": "User"
  }
  ```
- **Response:**
  ```json
  {
    "message": "User registered successfully",
    "user": {
      "id": 4,
      "username": "newuser",
      "email": "newuser@example.com",
      "first_name": "New",
      "last_name": "User",
      "date_joined": "2025-07-08T10:30:00Z"
    },
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "expires": "2025-07-08T11:30:00Z"
  }
  ```

### 2. Login
- **POST** `/api/auth/login/`
- **Request Body:**
  ```json
  {
    "username": "admin",
    "password": "admin123"
  }
  ```
- **Response:**
  ```json
  {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "expires": "2025-07-08T10:30:00Z"
  }
  ```

### 3. Verify Token
- **POST** `/api/auth/verify/`
- **Request Body:**
  ```json
  {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```
- **Response:**
  ```json
  {
    "valid": true,
    "message": "Token is valid"
  }
  ```

### 4. Validate Token
- **GET** `/api/auth/validate/`
- **Headers:**
  ```
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  ```
- **Response:**
  ```json
  {
    "valid": true,
    "user": "admin",
    "expires": "2025-07-08T10:30:00Z"
  }
  ```

### 5. API Documentation
- **GET** `/swagger/` - Interactive Swagger UI
- **GET** `/redoc/` - ReDoc documentation
- **GET** `/api/auth/health/` - Health check endpoint

## Sample User Credentials

- **admin** / **admin123**
- **testuser** / **testpass123**
- **demo** / **demo123**

## Local Development Setup

### Prerequisites
- Python 3.8+
- pip
- virtualenv

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd systemstake
   ```

2. **Set up virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run setup script:**
   ```bash
   ./setup.sh
   ```

4. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/api/auth/`

### Manual Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create sample users:**
   ```bash
   python manage.py create_sample_users
   ```

4. **Start server:**
   ```bash
   python manage.py runserver
   ```

## Docker Deployment

### Local Docker Setup

1. **Build the Docker image:**
   ```bash
   docker build -t jwt-auth-api .
   ```

2. **Run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

The API will be available at `http://localhost:8000/api/auth/`

### Production Docker Setup

1. **Update environment variables in docker-compose.yml:**
   ```yaml
   environment:
     - DEBUG=False
     - SECRET_KEY=your-production-secret-key
     - JWT_SECRET_KEY=your-production-jwt-secret
     - ALLOWED_HOSTS=your-domain.com,your-ec2-ip
   ```

2. **Deploy:**
   ```bash
   docker-compose up -d
   ```

## AWS EC2 Deployment

### Prerequisites
- AWS EC2 instance (Ubuntu 20.04 LTS recommended)
- Docker and Docker Compose installed on EC2
- Security group allowing inbound traffic on port 8000

### Deployment Steps

1. **Connect to your EC2 instance:**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

2. **Install Docker and Docker Compose:**
   ```bash
   sudo apt update
   sudo apt install -y docker.io docker-compose
   sudo usermod -aG docker ubuntu
   ```

3. **Clone and deploy:**
   ```bash
   git clone <repository-url>
   cd systemstake
   
   # Update environment variables for production
   nano docker-compose.yml
   
   # Deploy
   docker-compose up -d
   ```

4. **Initialize database:**
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py create_sample_users
   ```

Your API will be available at `http://your-ec2-ip:8000/api/auth/`

## Testing the API

### Using curl

1. **Register a new user:**
   ```bash
   curl -X POST http://localhost:8000/api/auth/register/ \
     -H "Content-Type: application/json" \
     -d '{
       "username": "newuser",
       "email": "newuser@example.com",
       "password": "securepassword123",
       "password_confirm": "securepassword123",
       "first_name": "New",
       "last_name": "User"
     }'
   ```

2. **Login:**
   ```bash
   curl -X POST http://localhost:8000/api/auth/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123"}'
   ```

3. **Verify token:**
   ```bash
   curl -X POST http://localhost:8000/api/auth/verify/ \
     -H "Content-Type: application/json" \
     -d '{"token": "YOUR_TOKEN_HERE"}'
   ```

4. **Validate token:**
   ```bash
   curl -X GET http://localhost:8000/api/auth/validate/ \
     -H "Authorization: Bearer YOUR_TOKEN_HERE"
   ```

### Using Python requests

```python
import requests

# Register a new user
response = requests.post('http://localhost:8000/api/auth/register/', json={
    'username': 'newuser',
    'email': 'newuser@example.com',
    'password': 'securepassword123',
    'password_confirm': 'securepassword123',
    'first_name': 'New',
    'last_name': 'User'
})
print(response.json())

# Login
response = requests.post('http://localhost:8000/api/auth/login/', 
                        json={'username': 'admin', 'password': 'admin123'})
token = response.json()['token']

# Verify
response = requests.post('http://localhost:8000/api/auth/verify/', 
                        json={'token': token})
print(response.json())

# Validate
response = requests.get('http://localhost:8000/api/auth/validate/', 
                       headers={'Authorization': f'Bearer {token}'})
print(response.json())
```

## Configuration

### Environment Variables

- `DEBUG`: Set to `False` for production
- `SECRET_KEY`: Django secret key
- `JWT_SECRET_KEY`: Secret key for JWT token signing
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### JWT Configuration

- Token expiration: 1 hour (3600 seconds)
- Algorithm: HS256
- Claims: user_id, username, exp, iat

## Security Features

- JWT tokens with expiration
- Secure token validation
- CORS support for cross-origin requests
- Input validation and sanitization
- Error handling without sensitive information exposure

## Project Structure

```
systemstake/
├── jwt_auth_api/           # Main Django project
│   ├── settings.py         # Django settings
│   ├── urls.py            # URL configuration
│   └── wsgi.py            # WSGI application
├── authentication/         # Authentication app
│   ├── views.py           # API views
│   ├── serializers.py     # Request/response serializers
│   ├── jwt_service.py     # JWT utility functions
│   └── urls.py            # App URL configuration
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── requirements.txt       # Python dependencies
├── setup.sh              # Setup script
└── README.md             # This file
```

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please create an issue in the GitHub repository.
