#!/usr/bin/env python3
"""
Debug script to test chat functionality
"""
import asyncio
from main import app
from fastapi.testclient import TestClient

def debug_chat():
    """Debug chat functionality"""
    print("Testing chat functionality with TestClient...")

    client = TestClient(app)

    # First, create a user
    print("\n1. Creating test user...")
    signup_response = client.post("/api/auth/signup", json={
        "email": "test2@example.com",
        "password": "testpass123",
        "name": "Test User 2"
    })
    print(f"Signup response: {signup_response.status_code}")

    if signup_response.status_code != 200:
        print(f"Signup failed: {signup_response.text}")
        return

    token_data = signup_response.json()
    token = token_data['data']['token']
    print("Token obtained successfully")

    # Test chat endpoint with auth
    print("\n2. Testing chat endpoint...")
    headers = {"Authorization": f"Bearer {token}"}

    # First message - should create conversation
    chat_response = client.post("/api/chat/",
                               json={"message": "Hello, how are you?"},
                               headers=headers)
    print(f"Chat response status: {chat_response.status_code}")

    if chat_response.status_code == 200:
        chat_data = chat_response.json()
        print(f"Chat response: {chat_data}")

        # Second message - should use existing conversation
        if 'conversation_id' in chat_data:
            conv_id = chat_data['conversation_id']
            print(f"\n3. Testing with conversation ID: {conv_id}")

            chat_response2 = client.post("/api/chat/",
                                        json={"message": "Add a task to buy milk", "conversation_id": conv_id},
                                        headers=headers)
            print(f"Second chat response status: {chat_response2.status_code}")
            if chat_response2.status_code == 200:
                print(f"Second chat response: {chat_response2.json()}")
            else:
                print(f"Second chat error: {chat_response2.text}")
    else:
        print(f"Chat error: {chat_response.text}")

if __name__ == "__main__":
    debug_chat()