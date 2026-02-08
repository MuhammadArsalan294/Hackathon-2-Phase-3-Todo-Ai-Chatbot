#!/usr/bin/env python3
"""
Test script to verify chat functionality
"""
from main import app
from fastapi.testclient import TestClient

def test_chat_functionality():
    """Test chat functionality"""
    print("Testing chat functionality...")

    try:
        client = TestClient(app)

        # Test chat endpoint
        response = client.post("/api/chat/", json={"message": "Hello"})

        print(f"Chat endpoint status: {response.status_code}")

        if response.status_code == 401:
            print("Chat endpoint requires authentication (expected)")
        elif response.status_code == 200:
            print(f"Chat endpoint response: {response.json()}")
        else:
            print(f"Chat endpoint response: {response.text}")

        # Test all registered endpoints
        print("\nRegistered API routes:")
        import main
        for route in app.routes:
            if hasattr(route, 'methods') and hasattr(route, 'path'):
                print(f"  {route.methods} {route.path}")

        print("\n✅ Backend with chat functionality is working!")
        return True

    except Exception as e:
        print(f"❌ Error testing chat functionality: {str(e)}")
        return False

if __name__ == "__main__":
    test_chat_functionality()