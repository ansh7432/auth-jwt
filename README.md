# JWT Authentication + MongoDB API

A Django REST Framework JWT authentication API with MongoDB integration, containerized with Docker and ready for deployment on Google Cloud Run.

---

## 🚀 Live Demo

**[View the API on GCP](https://auth-jwt-445166878228.europe-west1.run.app/)**

**[Walkthrough] : (https://www.loom.com/share/5fc93a4f479d496f91ae0687b597fd3b)**
---

## Features

- JWT-based authentication
- **MongoDB integration** with full CRUD operations
- User registration, login, token verify, and validate endpoints
- **Flexible document storage** in MongoDB Atlas
- **Query filtering and pagination** for MongoDB documents
- Interactive API docs: Swagger (`/swagger/`) & ReDoc (`/redoc/`)
- Dockerized for easy deployment

---

## API Endpoints

### Authentication Endpoints
| Method | Endpoint                | Description                |
|--------|-------------------------|----------------------------|
| POST   | `/api/auth/register/`   | Register a new user        |
| POST   | `/api/auth/login/`      | Obtain JWT token           |
| POST   | `/api/auth/verify/`     | Verify JWT token           |
| GET    | `/api/auth/validate/`   | Validate JWT token         |
| GET    | `/api/auth/health/`     | Health check               |

### MongoDB API Endpoints
| Method | Endpoint                           | Description                    |
|--------|------------------------------------|--------------------------------|
| GET    | `/api/mongodb/test-connection/`    | Test MongoDB connection        |
| POST   | `/api/mongodb/documents/create/`   | Create new document            |
| GET    | `/api/mongodb/documents/`          | Get documents (with filtering) |
| GET    | `/api/mongodb/documents/{id}/`     | Get specific document          |
| PUT    | `/api/mongodb/documents/{id}/update/` | Update document             |
| DELETE | `/api/mongodb/documents/{id}/delete/` | Delete document             |
| GET    | `/api/mongodb/stats/`              | Get collection statistics      |

### Documentation
| Method | Endpoint    | Description           |
|--------|-------------|-----------------------|
| GET    | `/swagger/` | Swagger API docs      |
| GET    | `/redoc/`   | ReDoc API docs        |

---

## Example Usage

### Authentication Examples

#### Register
```bash
curl -X POST https://auth-jwt-445166878228.europe-west1.run.app/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","email":"newuser@example.com","password":"securepassword123","password_confirm":"securepassword123"}'
```

#### Login
```bash
curl -X POST https://auth-jwt-445166878228.europe-west1.run.app/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","password":"securepassword123"}'
```

### MongoDB API Examples

#### Test MongoDB Connection
```bash
curl -X GET https://auth-jwt-445166878228.europe-west1.run.app/api/mongodb/test-connection/
```

#### Create Document
```bash
curl -X POST https://auth-jwt-445166878228.europe-west1.run.app/api/mongodb/documents/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "description": "Sample user document",
    "data": {
      "location": "New York",
      "skills": ["Python", "MongoDB", "Django"],
      "preferences": {
        "theme": "dark",
        "language": "en"
      }
    }
  }'
```

#### Get Documents with Filtering
```bash
curl -X GET "https://auth-jwt-445166878228.europe-west1.run.app/api/mongodb/documents/?name=John&limit=10&sort_order=desc" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Update Document
```bash
curl -X PUT https://auth-jwt-445166878228.europe-west1.run.app/api/mongodb/documents/DOCUMENT_ID/update/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "name": "John Smith",
    "age": 31
  }'
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
