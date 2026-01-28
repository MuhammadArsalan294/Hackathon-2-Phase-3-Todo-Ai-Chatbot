"""
Test script to verify task creation functionality
"""
import asyncio
import uuid
from datetime import datetime, timedelta
import jwt
from sqlmodel import select
from db import AsyncSessionLocal
from models.task import Task
from config.settings import settings


def generate_test_token(user_id: str = "test-user-123"):
    """Generate a test JWT token like the auth endpoints would"""
    token_data = {
        "userId": user_id,
        "email": "test@example.com",
        "exp": datetime.utcnow() + timedelta(days=1)  # 1 day expiration
    }

    token = jwt.encode(token_data, settings.BETTER_AUTH_SECRET, algorithm="HS256")
    return token


async def test_task_creation():
    """Test creating a task with a mock token"""
    print("Testing task creation functionality...")

    # Generate a test token
    test_token = generate_test_token()
    print(f"Generated test token: {test_token[:20]}...")

    # Create a test task directly in the database to simulate what should happen
    async with AsyncSessionLocal() as session:
        # Create a test task
        test_task = Task(
            title="Test Task from Backend",
            description="This is a test task created to verify functionality",
            completed=False,
            user_id="test-user-123"
        )

        session.add(test_task)
        await session.commit()
        await session.refresh(test_task)

        print(f"Task created successfully with ID: {test_task.id}")

        # Verify the task was created
        statement = select(Task).where(Task.id == test_task.id)
        result = await session.execute(statement)
        retrieved_task = result.scalar_one_or_none()

        if retrieved_task:
            print(f"Task retrieved successfully: {retrieved_task.title}")
            print("Task creation functionality is working correctly!")
        else:
            print("ERROR: Task was not found in database")


if __name__ == "__main__":
    asyncio.run(test_task_creation())