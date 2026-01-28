"""
Test script to verify the authentication endpoints work correctly
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_signup():
    print("Testing Signup Endpoint...")
    signup_data = {
        "email": "test@example.com",
        "password": "SecurePass123!",
        "name": "Test User"
    }

    response = requests.post(f"{BASE_URL}/api/auth/signup", json=signup_data)
    print(f"Signup Status: {response.status_code}")
    print(f"Signup Response: {response.json()}")
    return response.json()

def test_signin():
    print("\nTesting Signin Endpoint...")
    signin_data = {
        "email": "test@example.com",
        "password": "SecurePass123!"
    }

    response = requests.post(f"{BASE_URL}/api/auth/signin", json=signin_data)
    print(f"Signin Status: {response.status_code}")
    print(f"Signin Response: {response.json()}")
    return response.json()

def test_forgot_password():
    print("\nTesting Forgot Password Endpoint...")
    forgot_data = {
        "email": "test@example.com"
    }

    response = requests.post(f"{BASE_URL}/api/auth/forgot-password", json=forgot_data)
    print(f"Forgot Password Status: {response.status_code}")
    print(f"Forgot Password Response: {response.json()}")
    return response.json()

def test_logout():
    print("\nTesting Logout Endpoint...")
    response = requests.post(f"{BASE_URL}/api/auth/logout")
    print(f"Logout Status: {response.status_code}")
    print(f"Logout Response: {response.json()}")
    return response.json()

if __name__ == "__main__":
    print("Starting authentication flow tests...\n")

    # Test signup
    signup_result = test_signup()

    # Test signin
    signin_result = test_signin()

    # Test forgot password
    forgot_result = test_forgot_password()

    # Test logout
    logout_result = test_logout()

    print("\nAll authentication tests completed!")