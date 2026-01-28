"""
Script to test database connection and table creation
"""
import asyncio
from sqlmodel import select
from db import AsyncSessionLocal
from models.task import Task


async def test_database():
    """Test database connection and table creation"""
    print("Testing database connection and tables...")

    # Create a session using the session maker
    async with AsyncSessionLocal() as session:
        # Try to query the tasks table (should be empty initially)
        statement = select(Task)
        result = await session.execute(statement)
        tasks = result.scalars().all()

        print(f"Successfully connected to database!")
        print(f"Found {len(tasks)} tasks in the database (expected: 0)")
        print("Database and tables are working correctly!")


if __name__ == "__main__":
    asyncio.run(test_database())