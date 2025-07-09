# JWT Authentication API

A Django REST Framework JWT authentication API, containerized with Docker and ready for deployment on Google Cloud Run.

---

## 🚀 Live Demo

**[View the API on GCP](https://auth-jwt-445166878228.europe-west1.run.app/)**

**[Walkthrough] : (https://www.loom.com/share/5fc93a4f479d496f91ae0687b597fd3b)**
---

## Features

- JWT-based authentication
- User registration, login, token verify, and validate endpoints
- Interactive API docs: Swagger (`/swagger/`) & ReDoc (`/redoc/`)
- Dockerized for easy deployment

---

## API Endpoints

| Method | Endpoint                | Description                |
|--------|-------------------------|----------------------------|
| POST   | `/api/auth/register/`   | Register a new user        |
| POST   | `/api/auth/login/`      | Obtain JWT token           |
| POST   | `/api/auth/verify/`     | Verify JWT token           |
| GET    | `/api/auth/validate/`   | Validate JWT token         |
| GET    | `/api/auth/health/`     | Health check               |
| GET    | `/swagger/`             | Swagger API docs           |
| GET    | `/redoc/`               | ReDoc API docs             |

---

## Example Usage

### Register
```bash
curl -X POST https://auth-jwt-445166878228.europe-west1.run.app/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","email":"newuser@example.com","password":"securepassword123","password_confirm":"securepassword123"}'
```

### Login
```bash
curl -X POST https://auth-jwt-445166878228.europe-west1.run.app/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","password":"securepassword123"}'
```

---

## Local Development

```bash
git clone https://github.com/ansh7432/auth-jwt
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
API available at `http://localhost:8080/api/auth/`

---

## Docker

```bash
docker build -t jwt-auth-api .
docker run -p 8080:8080 jwt-auth-api
```
Or with Compose:
```bash
docker-compose up -d
```

---

## Configuration

Set these environment variables as needed:
- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`

---
