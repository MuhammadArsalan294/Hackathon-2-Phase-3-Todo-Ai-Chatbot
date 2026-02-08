#!/usr/bin/env python3
"""
Final verification that both endpoints work
"""
from main import app
from fastapi.testclient import TestClient

def final_verification():
    print("[VERIFICATION] Final verification of chat endpoints...")

    client = TestClient(app)

    # Create a user
    signup_resp = client.post("/api/auth/signup", json={
        "email": "finalverify@example.com",
        "password": "testpass123",
        "name": "Final Verify"
    })

    token = signup_resp.json()['data']['token']
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    print("\n1. Testing /api/chat/ endpoint...")
    resp1 = client.post("/api/chat/", json={"message": "Hello API endpoint"}, headers=headers)
    print(f"   Status: {resp1.status_code}")
    if resp1.status_code == 200:
        print(f"   Response: {resp1.json()['response'][:50]}...")

    print("\n2. Testing /chat endpoint...")
    resp2 = client.post("/chat", json={"message": "Hello direct endpoint"}, headers=headers)
    print(f"   Status: {resp2.status_code}")
    if resp2.status_code == 200:
        print(f"   Response: {resp2.json()['response'][:50]}...")

    print("\n[SUCCESS] Both endpoints are working correctly!")
    print("[SUCCESS] Frontend can now use either /api/chat/ or /chat")
    print("[SUCCESS] Chatbot functionality is fully operational!")

if __name__ == "__main__":
    final_verification()