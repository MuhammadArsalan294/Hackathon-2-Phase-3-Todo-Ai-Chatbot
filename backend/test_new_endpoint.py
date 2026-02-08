#!/usr/bin/env python3
"""
Test the new /chat endpoint
"""
from main import app
from fastapi.testclient import TestClient

def test_new_endpoint():
    """Test the new /chat endpoint"""
    print("Testing new /chat endpoint...")

    client = TestClient(app)

    # First, create a user to get a valid token
    signup_resp = client.post("/api/auth/signup", json={
        "email": "test5@example.com",
        "password": "testpass123",
        "name": "Test User 5"
    })

    if signup_resp.status_code != 200:
        print(f"Signup failed: {signup_resp.text}")
        return

    token = signup_resp.json()['data']['token']
    print("Got token successfully")

    # Test the new /chat endpoint
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    chat_resp = client.post("/chat",
                          json={"message": "Hello from new endpoint!"},
                          headers=headers)

    print(f"Response status: {chat_resp.status_code}")
    print(f"Response: {chat_resp.text}")

    # Also check all registered routes
    print("\nAll registered routes:")
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            if 'chat' in route.path.lower():
                print(f"  {route.methods} {route.path}")

if __name__ == "__main__":
    test_new_endpoint()