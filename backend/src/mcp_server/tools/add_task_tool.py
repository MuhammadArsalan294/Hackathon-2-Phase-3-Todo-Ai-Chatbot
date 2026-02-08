from typing import Dict, Any
from backend.src.mcp_server.server import mcp_server
from backend.src.services.sync_task_service import SyncTaskService
from backend.models.task import TaskCreate
from backend.db import get_session
from sqlmodel import Session


def add_task(title: str, description: str = None, user_id: str = None) -> Dict[str, Any]:
    """
    Create a new task for the authenticated user
    """
    # In a real implementation, user_id would come from the authentication context
    # For now, we'll accept it as a parameter for demonstration
    if not user_id:
        raise ValueError("user_id is required")

    # Create a new session for this operation
    with next(get_session()) as db_session:
        task_service = SyncTaskService(db_session)

        # Prepare the task data
        task_data = TaskCreate(
            title=title,
            description=description,
            completed=False
        )

        # Create the task
        task = task_service.create_task(task_data, user_id)

        return {
            "task_id": task.id,
            "status": "pending" if not task.completed else "completed",
            "title": task.title,
            "description": task.description or '',
            "message": f"Successfully created task: {task.title}"
        }


# Register the tool with the MCP server
mcp_server.register_tool(
    name="add_task",
    func=add_task,
    description="Create a new task for the authenticated user",
    parameters={
        "title": {
            "type": "string",
            "description": "Title of the task to create"
        },
        "description": {
            "type": "string",
            "description": "Optional description of the task"
        },
        "user_id": {
            "type": "string",
            "description": "ID of the user creating the task (derived from JWT context)"
        }
    }
)