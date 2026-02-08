from sqlmodel import create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config.settings import settings
from typing import AsyncGenerator, Generator
import contextlib


# Create engines for both sync and async
DATABASE_URL = settings.NEON_DATABASE_URL
sync_engine = create_engine(DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://"))
async_engine = create_async_engine(DATABASE_URL)

# Create session makers
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession
)

# Export the async engine for init_db.py
engine = async_engine

# Dependency to get sync session
def get_session() -> Generator[Session, None, None]:
    with SyncSessionLocal() as session:
        yield session


# Dependency to get async session
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session