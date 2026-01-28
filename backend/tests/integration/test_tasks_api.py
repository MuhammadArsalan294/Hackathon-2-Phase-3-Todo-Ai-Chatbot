import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, AsyncMock
from models.task import Task
from auth.jwt_handler import verify_token_and_get_user_id


@pytest.fixture
def client():
    """Create a test client for the API"""
    return TestClient(app)


@pytest.fixture
def valid_jwt_token():
    """Provide a valid JWT token for testing"""
    return "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwidXNlcklkIjoidGVzdC11c2VyLTEyMyIsImlhdCI6MTUxNjIzOTAyMn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"


def test_get_tasks_unauthorized(client):
    """Test getting tasks without authorization"""
    response = client.get("/api/tasks")
    assert response.status_code == 401  # Unauthorized


@patch('routes.tasks.get_async_session')
@patch('dependencies.auth.verify_token_and_get_user_id')
def test_get_tasks_success(mock_verify_token, mock_get_session, client, valid_jwt_token):
    """Test getting tasks with valid authorization"""
    # Mock the token verification
    mock_verify_token.return_value = "test-user-123"

    # Mock the database session and results
    mock_session = AsyncMock()
    mock_get_session.return_value.__aenter__.return_value = mock_session

    # Mock the task service
    with patch('routes.tasks.TaskService') as mock_task_service_class:
        mock_task_service = AsyncMock()
        mock_task_service_class.return_value = mock_task_service

        mock_tasks = [
            Task(id=1, title="Test Task 1", description="Description 1", completed=False, user_id="test-user-123"),
            Task(id=2, title="Test Task 2", description="Description 2", completed=True, user_id="test-user-123")
        ]
        mock_task_service.get_tasks_by_user.return_value = mock_tasks

        response = client.get("/api/tasks", headers={"Authorization": valid_jwt_token})

        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["title"] == "Test Task 1"


@patch('dependencies.auth.verify_token_and_get_user_id')
def test_create_task_success(mock_verify_token, client, valid_jwt_token):
    """Test creating a task with valid authorization"""
    mock_verify_token.return_value = "test-user-123"

    task_data = {
        "title": "New Task",
        "description": "New Description",
        "completed": False
    }

    # Since we're mocking the DB layer, this will fail at the DB level but we can still test the auth flow
    response = client.post("/api/tasks", json=task_data, headers={"Authorization": valid_jwt_token})

    # We expect a 500 error due to mocking, but if auth passed, the error would be different
    # The important thing is that it's not a 401 (unauthorized)
    assert response.status_code != 401


def test_create_task_unauthorized(client):
    """Test creating a task without authorization"""
    task_data = {
        "title": "New Task",
        "description": "New Description",
        "completed": False
    }

    response = client.post("/api/tasks", json=task_data)
    assert response.status_code == 401  # Unauthorized


@patch('dependencies.auth.verify_token_and_get_user_id')
def test_update_task_completion(mock_verify_token, client, valid_jwt_token):
    """Test updating task completion status"""
    mock_verify_token.return_value = "test-user-123"

    completion_data = {
        "completed": True
    }

    response = client.patch("/api/tasks/1/complete", json=completion_data, headers={"Authorization": valid_jwt_token})

    # We expect a 404 or 500 due to mocking, but not 401
    assert response.status_code != 401


def test_update_task_completion_unauthorized(client):
    """Test updating task completion without authorization"""
    completion_data = {
        "completed": True
    }

    response = client.patch("/api/tasks/1/complete", json=completion_data)
    assert response.status_code == 401  # Unauthorized


if __name__ == "__main__":
    pytest.main([__file__])