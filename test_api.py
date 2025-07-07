#!/usr/bin/env python3
"""
Test script for JWT Authentication API
"""

import requests
import json
import sys
import time

# API base URL
BASE_URL = "http://localhost:8000/api/auth"

def test_api():
    print("Testing JWT Authentication API...")
    print("=" * 50)
    
    # Test data
    test_credentials = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        # Test 1: Login
        print("1. Testing Login...")
        login_response = requests.post(
            f"{BASE_URL}/login/",
            json=test_credentials,
            headers={"Content-Type": "application/json"}
        )
        
        if login_response.status_code == 200:
            login_data = login_response.json()
            token = login_data.get("token")
            expires = login_data.get("expires")
            print(f"   ✓ Login successful")
            print(f"   Token: {token[:50]}...")
            print(f"   Expires: {expires}")
        else:
            print(f"   ✗ Login failed: {login_response.status_code}")
            print(f"   Response: {login_response.text}")
            return False
        
        # Test 2: Verify Token
        print("\n2. Testing Token Verification...")
        verify_response = requests.post(
            f"{BASE_URL}/verify/",
            json={"token": token},
            headers={"Content-Type": "application/json"}
        )
        
        if verify_response.status_code == 200:
            verify_data = verify_response.json()
            print(f"   ✓ Token verification successful")
            print(f"   Valid: {verify_data.get('valid')}")
            print(f"   Message: {verify_data.get('message')}")
        else:
            print(f"   ✗ Token verification failed: {verify_response.status_code}")
            print(f"   Response: {verify_response.text}")
            return False
        
        # Test 3: Validate Token
        print("\n3. Testing Token Validation...")
        validate_response = requests.get(
            f"{BASE_URL}/validate/",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if validate_response.status_code == 200:
            validate_data = validate_response.json()
            print(f"   ✓ Token validation successful")
            print(f"   Valid: {validate_data.get('valid')}")
            print(f"   User: {validate_data.get('user')}")
            print(f"   Expires: {validate_data.get('expires')}")
        else:
            print(f"   ✗ Token validation failed: {validate_response.status_code}")
            print(f"   Response: {validate_response.text}")
            return False
        
        # Test 4: Test with invalid token
        print("\n4. Testing with Invalid Token...")
        invalid_verify_response = requests.post(
            f"{BASE_URL}/verify/",
            json={"token": "invalid.token.here"},
            headers={"Content-Type": "application/json"}
        )
        
        if invalid_verify_response.status_code == 200:
            invalid_data = invalid_verify_response.json()
            if not invalid_data.get('valid'):
                print(f"   ✓ Invalid token correctly rejected")
                print(f"   Message: {invalid_data.get('message')}")
            else:
                print(f"   ✗ Invalid token was accepted (should not happen)")
                return False
        else:
            print(f"   ✗ Invalid token test failed: {invalid_verify_response.status_code}")
            return False
        
        # Test 5: Test with invalid credentials
        print("\n5. Testing with Invalid Credentials...")
        invalid_login_response = requests.post(
            f"{BASE_URL}/login/",
            json={"username": "invalid", "password": "invalid"},
            headers={"Content-Type": "application/json"}
        )
        
        if invalid_login_response.status_code == 401:
            print(f"   ✓ Invalid credentials correctly rejected")
        else:
            print(f"   ✗ Invalid credentials test failed: {invalid_login_response.status_code}")
            return False
        
        print("\n" + "=" * 50)
        print("All tests passed! 🎉")
        return True
        
    except requests.exceptions.ConnectionError:
        print("   ✗ Connection failed. Make sure the server is running.")
        print("   Run: python manage.py runserver")
        return False
    except Exception as e:
        print(f"   ✗ Test failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)
