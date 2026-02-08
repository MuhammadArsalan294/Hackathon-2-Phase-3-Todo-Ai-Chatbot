#!/usr/bin/env python3
"""
Test script to isolate the chat functionality issue
"""
import traceback
from main import app
from fastapi.testclient import TestClient

def test_isolated():
    """Test isolated functionality"""
    print("Testing isolated chat functionality...")

    try:
        client = TestClient(app)

        # Test a simple signup
        print("\nTesting signup...")
        signup_resp = client.post("/api/auth/signup", json={
            "email": "test4@example.com",
            "password": "testpass123",
            "name": "Test User 4"
        })
        print(f"Signup status: {signup_resp.status_code}")

        if signup_resp.status_code == 200:
            data = signup_resp.json()
            print(f"Signup response keys: {list(data.keys()) if data else 'None'}")

            if 'data' in data and data['data'] and 'token' in data['data']:
                token = data['data']['token']
                print("Token obtained, testing chat...")

                # Test chat with new conversation (no conversation_id provided)
                chat_resp = client.post("/api/chat/",
                                      json={"message": "Hello test"},
                                      headers={"Authorization": f"Bearer {token}"})
                print(f"Chat response status: {chat_resp.status_code}")

                if chat_resp.status_code != 200:
                    print(f"Chat response: {chat_resp.text}")

                    # Try to get more details by looking at the app routes
                    print("\nChecking registered routes...")
                    for route in app.routes:
                        if hasattr(route, 'path') and 'chat' in getattr(route, 'path', ''):
                            print(f"Found chat route: {route.path}")

            else:
                print("No token in response")
        else:
            print(f"Signup failed: {signup_resp.text}")

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        print("Full traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    test_isolated()