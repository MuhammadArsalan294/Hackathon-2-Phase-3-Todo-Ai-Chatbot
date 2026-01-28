#!/usr/bin/env python
"""
Test script to check the API endpoints directly
"""

import requests
import time
import json

BASE_URL = "http://localhost:8000"

# Wait a moment for the server to start
print("Waiting for server to start...")
time.sleep(3)

def test_api_call(endpoint, data=None, method='POST'):
    """Helper function to make API calls"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\nMaking {method} request to: {url}")
    if data:
        print(f"Data: {json.dumps(data, indent=2)}")

    try:
        if method.upper() == 'POST':
            response = requests.post(url, json=data, timeout=10)
        elif method.upper() == 'GET':
            response = requests.get(url, timeout=10)
        else:
            raise ValueError(f"Unsupported method: {method}")

        print(f"Status: {response.status_code}")
        try:
            response_json = response.json()
            print(f"Response: {json.dumps(response_json, indent=2)}")
        except:
            print(f"Response text: {response.text}")

        return response
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to server. Is it running?")
        return None
    except Exception as e:
        print(f"ERROR: {e}")
        return None

print("Testing authentication endpoints...")

# Test the server health first
print("\n1. Testing server health...")
health_response = test_api_call("/health", method='GET')

# Test signup
print("\n2. Testing signup...")
signup_data = {
    "email": "test@example.com",
    "password": "SecurePass123!",
    "name": "Test User"
}
signup_response = test_api_call("/api/auth/signup", signup_data)

# Test signin
print("\n3. Testing signin...")
signin_data = {
    "email": "test@example.com",
    "password": "SecurePass123!"
}
signin_response = test_api_call("/api/auth/signin", signin_data)

# Test forgot password
print("\n4. Testing forgot password...")
forgot_data = {
    "email": "test@example.com"
}
forgot_response = test_api_call("/api/auth/forgot-password", forgot_data)

# Test logout
print("\n5. Testing logout...")
logout_response = test_api_call("/api/auth/logout")

print("\nAll tests completed!")