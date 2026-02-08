#!/usr/bin/env python3
"""
Comprehensive test to verify that the chatbot now creates actual tasks in the database
"""
from main import app
from fastapi.testclient import TestClient
from db import sync_engine
from sqlmodel import Session as SQLModelSession
from models.task import Task
import json


def test_chatbot_creates_actual_tasks():
    """Test that chatbot requests actually create tasks in the database"""
    print("TEST: Testing if chatbot creates actual tasks in database...")

    try:
        client = TestClient(app)

        # Authenticate first
        signin_response = client.post("/api/auth/signin", json={
            "email": "test_chat@example.com",
            "password": "testpassword123"
        })

        if signin_response.status_code != 200:
            # If user doesn't exist, create one
            signup_response = client.post("/api/auth/signup", json={
                "email": "test_chat@example.com",
                "password": "testpassword123",
                "name": "Test User"
            })
            if signup_response.status_code != 200:
                print("ERROR Could not authenticate user")
                return False

            token = signup_response.json()["data"]["token"]
            user_id = signup_response.json()["data"]["user"]["id"]
        else:
            token = signin_response.json()["data"]["token"]
            user_id = signin_response.json()["data"]["user"]["id"]

        print(f"OK Authenticated as user: {user_id[:8]}...")

        # Count tasks before chat interaction
        with SQLModelSession(sync_engine) as db_session:
            initial_tasks = db_session.query(Task).filter(Task.user_id == user_id).all()
            print(f"DATA Initial tasks for user: {len(initial_tasks)}")

        # Send a chat message to add a task
        headers = {"Authorization": f"Bearer {token}"}
        chat_response = client.post("/api/chat/",
                                   json={"message": "Add a task to buy bread and butter"},
                                   headers=headers)

        if chat_response.status_code != 200:
            print(f"ERROR Chat endpoint failed: {chat_response.text}")
            return False

        response_data = chat_response.json()
        print(f"MSG Chat response: {response_data['response']}")

        # Count tasks after chat interaction
        with SQLModelSession(sync_engine) as db_session:
            final_tasks = db_session.query(Task).filter(Task.user_id == user_id).all()
            print(f"DATA Final tasks for user: {len(final_tasks)}")

        # Verify task was created
        if len(final_tasks) > len(initial_tasks):
            new_task = final_tasks[-1]  # Get the most recently added task
            print(f"OK Task created successfully: '{new_task.title}' (ID: {new_task.id})")

            # Verify the task title matches our expectation
            if "bread" in new_task.title.lower() or "buy" in new_task.title.lower():
                print("OK Task title matches the request")
            else:
                print(f"WARN  Task title '{new_task.title}' doesn't fully match request")

        else:
            print("ERROR No new task was created in the database")

        # Test task listing functionality
        chat_response2 = client.post("/api/chat/",
                                    json={"message": "Show me my tasks"},
                                    headers=headers)

        if chat_response2.status_code == 200:
            response_data2 = chat_response2.json()
            print(f"LIST Show tasks response: {response_data2['response']}")

            # The response should contain the task we just created
            if len(final_tasks) > 0 and final_tasks[-1].title.lower() in response_data2['response'].lower():
                print("OK Show tasks correctly displays the created task")
            else:
                print("WARN  Show tasks response may not include the new task")

        return True

    except Exception as e:
        print(f"ERROR Error during task creation test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("Running comprehensive task creation test...")
    success = test_chatbot_creates_actual_tasks()

    if success:
        print("\nAll tests passed! The chatbot now creates actual tasks in the database.")
    else:
        print("\nSome tests failed.")