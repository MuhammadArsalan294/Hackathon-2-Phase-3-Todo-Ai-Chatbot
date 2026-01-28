import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from models.task import Task, TaskCreate, TaskUpdate
from services.task_service import TaskService
from utils.errors import ResourceNotFoundError


@pytest.mark.asyncio
async def test_create_task():
    """Test creating a new task"""
    # Mock session
    mock_session = AsyncMock(spec=AsyncSession)

    # Create service instance
    service = TaskService(mock_session)

    # Test data
    task_data = TaskCreate(title="Test Task", description="Test Description", completed=False)
    user_id = "user123"

    # Mock the add, commit, and refresh methods
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    # Create a mock task object to return
    mock_task = Task(id=1, title=task_data.title, description=task_data.description,
                     completed=task_data.completed, user_id=user_id)

    # Patch the Task constructor to return our mock with id set
    original_init = Task.__init__
    def mock_init(self, **kwargs):
        original_init(self, **{k: v for k, v in kwargs.items() if k != 'id'})
        self.id = 1  # Simulate auto-increment
    Task.__init__ = mock_init

    result = await service.create_task(task_data, user_id)

    # Assertions
    assert result.title == task_data.title
    assert result.description == task_data.description
    assert result.completed == task_data.completed
    assert result.user_id == user_id
    assert result.id == 1

    # Verify session methods were called
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_get_tasks_by_user():
    """Test getting all tasks for a user"""
    mock_session = AsyncMock(spec=AsyncSession)
    service = TaskService(mock_session)

    user_id = "user123"
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [
        Task(id=1, title="Task 1", description="Desc 1", completed=False, user_id=user_id),
        Task(id=2, title="Task 2", description="Desc 2", completed=True, user_id=user_id)
    ]
    mock_session.execute.return_value = mock_result

    result = await service.get_tasks_by_user(user_id)

    assert len(result) == 2
    assert result[0].title == "Task 1"
    assert result[1].completed is True


@pytest.mark.asyncio
async def test_get_task_by_id_success():
    """Test getting a task by ID successfully"""
    mock_session = AsyncMock(spec=AsyncSession)
    service = TaskService(mock_session)

    task_id = 1
    user_id = "user123"
    expected_task = Task(id=task_id, title="Test Task", description="Test Desc",
                         completed=False, user_id=user_id)

    mock_result = MagicMock()
    mock_result.scalar_one.return_value = expected_task
    mock_session.execute.return_value = mock_result

    result = await service.get_task_by_id(task_id, user_id)

    assert result.id == task_id
    assert result.user_id == user_id
    assert result.title == "Test Task"


@pytest.mark.asyncio
async def test_get_task_by_id_not_found():
    """Test getting a task by ID that doesn't exist"""
    mock_session = AsyncMock(spec=AsyncSession)
    service = TaskService(mock_session)

    from sqlalchemy.exc import NoResultFound
    mock_result = MagicMock()
    mock_result.scalar_one.side_effect = NoResultFound()
    mock_session.execute.return_value = mock_result

    with pytest.raises(ResourceNotFoundError):
        await service.get_task_by_id(999, "user123")


@pytest.mark.asyncio
async def test_update_task():
    """Test updating a task"""
    mock_session = AsyncMock(spec=AsyncSession)
    service = TaskService(mock_session)

    task_id = 1
    user_id = "user123"
    task_data = TaskUpdate(title="Updated Title", completed=True)

    # Create the existing task
    existing_task = Task(id=task_id, title="Original Title", description="Original Desc",
                         completed=False, user_id=user_id)

    mock_result = MagicMock()
    mock_result.scalar_one.return_value = existing_task
    mock_session.execute.return_value = mock_result
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    result = await service.update_task(task_id, task_data, user_id)

    # Check that the values were updated
    assert result.title == "Updated Title"
    assert result.completed is True
    assert result.description == "Original Desc"  # Unchanged

    # Verify session methods were called
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_delete_task():
    """Test deleting a task"""
    mock_session = AsyncMock(spec=AsyncSession)
    service = TaskService(mock_session)

    task_id = 1
    user_id = "user123"

    # Create the task to delete
    task_to_delete = Task(id=task_id, title="Task to Delete", description="Desc",
                          completed=False, user_id=user_id)

    mock_result = MagicMock()
    mock_result.scalar_one.return_value = task_to_delete
    mock_session.execute.return_value = mock_result
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()

    result = await service.delete_task(task_id, user_id)

    assert result is True
    mock_session.delete.assert_awaited_once_with(task_to_delete)
    mock_session.commit.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])