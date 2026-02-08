#!/usr/bin/env python3
"""
Test script to verify connection to Neon database and chat functionality
"""
from main import app
from fastapi.testclient import TestClient
from src.models.conversation import Conversation
from src.models.message import Message
from src.services.conversation_service import conversation_service
from src.services.chat_service import chat_service
from db import get_session, sync_engine
from sqlmodel import Session as SQLModelSession
import json


def test_neon_database_connection():
    """Test if we can connect to Neon database"""
    print("Testing Neon database connection...")

    try:
        # Test DB session creation
        with SQLModelSession(sync_engine) as session:
            # Try to query conversations table
            conversations = session.query(Conversation).limit(1).all()
            print(f"Successfully connected to Neon database")
            print(f"Found {len(conversations)} existing conversations")
            return True
    except Exception as e:
        print(f"X Failed to connect to Neon database: {str(e)}")
        return False


def test_chat_functionality():
    """Test chat functionality with Neon database"""
    print("\nTesting chat functionality with Neon database...")

    try:
        client = TestClient(app)

        # First, try to create a test user by signing up
        signup_response = client.post("/api/auth/signup", json={
            "email": "test_chat@example.com",
            "password": "testpassword123",
            "name": "Test User"
        })

        # Check if user already exists (which is fine)
        token = None
        if signup_response.status_code == 200:
            signup_data = signup_response.json()
            print(f"Signup response: {signup_data}")  # Debug print

            # Check if response has the expected structure
            if "data" in signup_data and signup_data["data"] and "token" in signup_data["data"]:
                token = signup_data["data"]["token"]

        # If signup failed because user exists, try to sign in
        if not token:
            signin_response = client.post("/api/auth/signin", json={
                "email": "test_chat@example.com",
                "password": "testpassword123"
            })

            if signin_response.status_code == 200:
                signin_data = signin_response.json()
                print(f"Signin response: {signin_data}")  # Debug print

                if "data" in signin_data and signin_data["data"] and "token" in signin_data["data"]:
                    token = signin_data["data"]["token"]

        if not token:
            print(f"X No token received from either signup or signin")
            return False

        print(f"OK User authenticated, token: {token[:10]}...")

        # Test chat endpoint with authentication
        headers = {"Authorization": f"Bearer {token}"}
        chat_response = client.post("/api/chat/",
                                   json={"message": "Hello, I want to add a task to buy milk"},
                                   headers=headers)

        print(f"Chat endpoint status: {chat_response.status_code}")

        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"OK Chat response: {response_data}")

            # Verify that the conversation was saved to Neon database
            with SQLModelSession(sync_engine) as session:
                conversation_id = response_data.get("conversation_id")
                if conversation_id:
                    # Check if conversation exists in database
                    conversation = session.get(Conversation, conversation_id)
                    if conversation:
                        print(f"OK Conversation {conversation_id} saved to Neon database")

                        # Check if messages were saved
                        messages = session.query(Message).filter(
                            Message.conversation_id == conversation_id
                        ).all()
                        print(f"OK Found {len(messages)} messages in conversation {conversation_id}")
                    else:
                        print(f"X Conversation {conversation_id} not found in database")
                else:
                    print("X No conversation_id returned from chat endpoint")

            return True
        else:
            print(f"X Chat endpoint failed: {chat_response.text}")
            return False

    except Exception as e:
        print(f"X Error testing chat functionality: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function"""
    print("Starting Neon database and chat functionality test...\n")

    # Test database connection
    db_ok = test_neon_database_connection()

    if not db_ok:
        print("\nX Database connection failed, stopping tests")
        return

    # Test chat functionality
    chat_ok = test_chat_functionality()

    if db_ok and chat_ok:
        print("\nAll tests passed! Neon database and chat functionality are working correctly.")
        return True
    else:
        print("\nX Some tests failed.")
        return False


if __name__ == "__main__":
    main()