from sqlmodel import create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config.settings import settings
from typing import AsyncGenerator


# Create async engine for Neon PostgreSQL
DATABASE_URL = settings.NEON_DATABASE_URL
engine = create_async_engine(DATABASE_URL)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)


# Dependency to get async session
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session