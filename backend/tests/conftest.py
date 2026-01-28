import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def mock_async_session():
    """Mock async database session for testing"""
    session = AsyncMock(spec=AsyncSession)
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.delete = MagicMock()
    return session


@pytest.fixture
def mock_task_data():
    """Sample task data for testing"""
    return {
        "title": "Test Task",
        "description": "Test Description",
        "completed": False
    }


@pytest.fixture
def mock_user_id():
    """Sample user ID for testing"""
    return "test-user-123"