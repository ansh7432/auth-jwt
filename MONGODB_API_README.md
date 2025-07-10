# JWT Authentication + MongoDB API

This Django project provides JWT-based authentication with MongoDB integration for document operations.

## Features

- **JWT Authentication**: User registration, login, and token-based authentication
- **MongoDB Integration**: Direct MongoDB operations using PyMongo
- **RESTful API**: Complete CRUD operations for documents
- **Swagger Documentation**: Interactive API documentation
- **Flexible Data Storage**: Store any JSON data in MongoDB collections

## MongoDB Configuration

The project is configured to connect to MongoDB Atlas with the following settings:

```python
MONGODB_CONFIG = {
    'host': 'mongodb+srv://ansh743:Anshsoni@123@db.zenpcjo.mongodb.net/',
    'database': 'auth_jwt_db',
    'options': {
        'authSource': 'admin',
        'authMechanism': 'SCRAM-SHA-1',
    }
}
```

## API Endpoints

### Authentication Endpoints
- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - Login and get JWT token
- `POST /api/auth/verify/` - Verify JWT token
- `GET /api/auth/validate/` - Validate JWT token
- `GET /api/auth/health/` - Health check

### MongoDB API Endpoints
- `GET /api/mongodb/test-connection/` - Test MongoDB connection
- `POST /api/mongodb/documents/create/` - Create a new document
- `GET /api/mongodb/documents/` - Get documents with filtering and pagination
- `GET /api/mongodb/documents/{id}/` - Get a specific document by ID
- `PUT /api/mongodb/documents/{id}/update/` - Update a document
- `DELETE /api/mongodb/documents/{id}/delete/` - Delete a document
- `GET /api/mongodb/stats/` - Get collection statistics

## Installation and Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Start the Server**:
   ```bash
   python manage.py runserver
   ```

## Usage Examples

### 1. Register a User
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'
```

### 2. Login and Get Token
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

### 3. Test MongoDB Connection
```bash
curl -X GET http://127.0.0.1:8000/api/mongodb/test-connection/
```

### 4. Create a Document
```bash
curl -X POST http://127.0.0.1:8000/api/mongodb/documents/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "description": "Test user document",
    "data": {
      "location": "New York",
      "interests": ["technology", "sports", "music"]
    }
  }'
```

### 5. Get Documents with Filtering
```bash
curl -X GET "http://127.0.0.1:8000/api/mongodb/documents/?name=John&limit=10&skip=0&sort_by=created_at&sort_order=desc" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 6. Update a Document
```bash
curl -X PUT http://127.0.0.1:8000/api/mongodb/documents/DOCUMENT_ID/update/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "name": "John Smith",
    "age": 31
  }'
```

### 7. Delete a Document
```bash
curl -X DELETE http://127.0.0.1:8000/api/mongodb/documents/DOCUMENT_ID/delete/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 8. Get Collection Statistics
```bash
curl -X GET http://127.0.0.1:8000/api/mongodb/stats/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Document Structure

Documents stored in MongoDB can have the following structure:

```json
{
  "_id": "ObjectId",
  "name": "string",
  "email": "string",
  "age": "number",
  "description": "string",
  "data": "object",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## Query Parameters for GET /api/mongodb/documents/

- `collection` (string): Collection name (default: 'user_data')
- `limit` (integer): Number of documents to return (default: 10, max: 100)
- `skip` (integer): Number of documents to skip (default: 0)
- `sort_by` (string): Field to sort by (default: 'created_at')
- `sort_order` (string): Sort order - 'asc' or 'desc' (default: 'desc')
- `name` (string): Filter by name (case-insensitive partial match)
- `email` (string): Filter by email (exact match)
- `age_min` (integer): Minimum age filter
- `age_max` (integer): Maximum age filter

## Testing

Run the test script to verify the API functionality:

```bash
python test_mongodb_api.py
```

## MongoDB Collections

The API uses the following collections:

- `user_data`: Main collection for storing user documents
- Additional collections can be specified in the query parameters

## Security

- All MongoDB operations (except connection test) require JWT authentication
- JWT tokens are validated on each request
- MongoDB credentials are stored in settings configuration

## API Documentation

Access the interactive API documentation at:
- Swagger UI: http://127.0.0.1:8000/swagger/
- ReDoc: http://127.0.0.1:8000/redoc/

## Error Handling

The API returns consistent error responses:

```json
{
  "status": "error",
  "message": "Error description",
  "errors": "Detailed error information (if applicable)"
}
```

## Success Responses

Successful responses follow this format:

```json
{
  "status": "success",
  "message": "Operation description",
  "data": "Response data"
}
```
