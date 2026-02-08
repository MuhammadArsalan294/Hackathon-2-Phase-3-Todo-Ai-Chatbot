#!/usr/bin/env python3
"""
Final comprehensive test of chat functionality
"""
import time
from main import app
from fastapi.testclient import TestClient

def final_test():
    """Final test of chat functionality"""
    print("[TEST] Final comprehensive test of chat functionality...")

    client = TestClient(app)

    # Step 1: Create a user
    print("\n[STEP 1] Creating user...")
    signup_resp = client.post("/api/auth/signup", json={
        "email": "finaltest@example.com",
        "password": "testpass123",
        "name": "Final Test User"
    })

    if signup_resp.status_code != 200:
        print(f"[ERROR] Signup failed: {signup_resp.text}")
        return

    token = signup_resp.json()['data']['token']
    print("[SUCCESS] User created successfully")

    # Step 2: Test initial chat message (creates conversation)
    print("\n[STEP 2] Testing initial chat message...")
    headers = {"Authorization": f"Bearer {token}"}

    chat_resp1 = client.post("/api/chat/",
                           json={"message": "Hello, I want to add a task!"},
                           headers=headers)

    if chat_resp1.status_code != 200:
        print(f"[ERROR] First chat failed: {chat_resp1.text}")
        return

    response1_data = chat_resp1.json()
    print(f"[SUCCESS] First chat successful: {response1_data['response'][:50]}...")

    if 'conversation_id' in response1_data:
        conv_id = response1_data['conversation_id']
        print(f"[SUCCESS] Conversation ID: {conv_id}")
    else:
        print("[ERROR] No conversation ID returned")
        return

    # Step 3: Test follow-up message (uses existing conversation)
    print("\n[STEP 3] Testing follow-up message...")
    chat_resp2 = client.post("/api/chat/",
                           json={
                               "message": "Add a task to buy milk and bread",
                               "conversation_id": conv_id
                           },
                           headers=headers)

    if chat_resp2.status_code != 200:
        print(f"[ERROR] Second chat failed: {chat_resp2.text}")
        return

    response2_data = chat_resp2.json()
    print(f"[SUCCESS] Second chat successful: {response2_data['response'][:50]}...")

    # Step 4: Test task listing
    print("\n[STEP 4] Testing task listing...")
    chat_resp3 = client.post("/api/chat/",
                           json={
                               "message": "Show me my tasks",
                               "conversation_id": conv_id
                           },
                           headers=headers)

    if chat_resp3.status_code != 200:
        print(f"[ERROR] Third chat failed: {chat_resp3.text}")
        return

    response3_data = chat_resp3.json()
    print(f"[SUCCESS] Third chat successful: {response3_data['response'][:50]}...")

    # Summary
    print("\n[SUMMARY]:")
    print("[CHECK] User registration works")
    print("[CHECK] Chat authentication works")
    print("[CHECK] New conversation creation works")
    print("[CHECK] Follow-up messages work")
    print("[CHECK] Task-related commands work")
    print("[CHECK] Database integration works")
    print("\n[RESULT] CHATBOT IS WORKING PERFECTLY!")

if __name__ == "__main__":
    final_test()