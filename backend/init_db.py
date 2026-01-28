"""
Script to initialize the database and create tables
"""
import asyncio
from sqlmodel import SQLModel
from db import engine
from models.task import Task


async def create_tables():
    """Create all database tables"""
    print("Creating database tables...")

    # Create all tables defined in SQLModel registry
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    print("Database tables created successfully!")


if __name__ == "__main__":
    asyncio.run(create_tables())