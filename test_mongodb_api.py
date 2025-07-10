#!/usr/bin/env python3

import requests
import json
import sys

# API base URL
BASE_URL = "http://127.0.0.1:8000"

def test_mongodb_connection():
    """Test MongoDB connection"""
    print("Testing MongoDB connection...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/mongodb/test-connection/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing MongoDB connection: {e}")
        return False

def register_user(username, email, password):
    """Register a new user"""
    print(f"Registering user: {username}")
    
    data = {
        "username": username,
        "email": email,
        "password": password,
        "password_confirm": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register/", json=data)
        print(f"Registration Status Code: {response.status_code}")
        print(f"Registration Response: {json.dumps(response.json(), indent=2)}")
        
        # User already exists is also considered success for this test
        if response.status_code == 201:
            return True
        elif response.status_code == 400:
            result = response.json()
            if "username" in result.get("details", {}) and "already exists" in str(result.get("details", {})):
                print("User already exists - proceeding with login test")
                return True
        
        return False
    except Exception as e:
        print(f"Error registering user: {e}")
        return False

def login_user(username, password):
    """Login user and get JWT token"""
    print(f"Logging in user: {username}")
    
    data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login/", json=data)
        print(f"Login Status Code: {response.status_code}")
        result = response.json()
        print(f"Login Response: {json.dumps(result, indent=2)}")
        
        if response.status_code == 200:
            return result.get('token') or result.get('access_token')
        return None
    except Exception as e:
        print(f"Error logging in user: {e}")
        return None

def create_document(token, data):
    """Create a document in MongoDB"""
    print("Creating document in MongoDB...")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/mongodb/documents/create/", 
                               json=data, headers=headers)
        print(f"Create Document Status Code: {response.status_code}")
        result = response.json()
        print(f"Create Document Response: {json.dumps(result, indent=2)}")
        return result.get('data', {}).get('id') if response.status_code == 201 else None
    except Exception as e:
        print(f"Error creating document: {e}")
        return None

def get_documents(token):
    """Get documents from MongoDB"""
    print("Getting documents from MongoDB...")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(f"{BASE_URL}/api/mongodb/documents/", headers=headers)
        print(f"Get Documents Status Code: {response.status_code}")
        result = response.json()
        print(f"Get Documents Response: {json.dumps(result, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error getting documents: {e}")
        return False

def main():
    """Main test function"""
    import random
    import string
    
    print("=" * 60)
    print("JWT Authentication + MongoDB API Test")
    print("=" * 60)
    
    # Test MongoDB connection
    if not test_mongodb_connection():
        print("❌ MongoDB connection test failed!")
        return
    
    print("✅ MongoDB connection test passed!")
    print("-" * 60)
    
    # Test user registration with unique username
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    test_user = {
        "username": f"testuser_{random_suffix}",
        "email": f"test_{random_suffix}@example.com",
        "password": "testpass123"
    }
    
    if not register_user(test_user["username"], test_user["email"], test_user["password"]):
        print("❌ User registration failed!")
        return
    
    print("✅ User registration passed!")
    print("-" * 60)
    
    # Test user login
    token = login_user(test_user["username"], test_user["password"])
    if not token:
        print("❌ User login failed!")
        return
    
    print("✅ User login passed!")
    print("-" * 60)
    
    # Test document creation
    test_document = {
        "name": "John Doe",
        "email": f"john_{random_suffix}@example.com",
        "age": 30,
        "description": "Test user document",
        "data": {
            "location": "New York",
            "interests": ["technology", "sports", "music"]
        }
    }
    
    document_id = create_document(token, test_document)
    if not document_id:
        print("❌ Document creation failed!")
        return
    
    print("✅ Document creation passed!")
    print("-" * 60)
    
    # Test getting documents
    if not get_documents(token):
        print("❌ Get documents failed!")
        return
    
    print("✅ Get documents passed!")
    print("-" * 60)
    
    print("🎉 All tests passed! The JWT Authentication + MongoDB API is working correctly!")

if __name__ == "__main__":
    main()
