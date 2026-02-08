from typing import Dict, Any
from backend.src.mcp_server.server import mcp_server
from backend.src.services.sync_task_service import SyncTaskService
from backend.models.task import TaskUpdate
from backend.db import get_session


def update_task(task_id: int, title: str = None, description: str = None, user_id: str = None) -> Dict[str, Any]:
    """
    Update task title and/or description for the authenticated user
    """
    if not user_id:
        raise ValueError("user_id is required")

    if not task_id:
        raise ValueError("task_id is required")

    if title is None and description is None:
        raise ValueError("At least one of title or description must be provided for update")

    # Create a new session for this operation
    with next(get_session()) as db_session:
        task_service = SyncTaskService(db_session)

        # Prepare update data using TaskUpdate model
        update_data = TaskUpdate()
        if title is not None:
            update_data.title = title
        if description is not None:
            update_data.description = description

        # Update the task
        updated_task = task_service.update_task(task_id, update_data, user_id)

        return {
            "task_id": updated_task.id,
            "status": "completed" if updated_task.completed else "pending",
            "title": updated_task.title,
            "message": f"Successfully updated task '{updated_task.title}'"
        }


# Register the tool with the MCP server
mcp_server.register_tool(
    name="update_task",
    func=update_task,
    description="Update task title and/or description. Validates ownership.",
    parameters={
        "task_id": {
            "type": "integer",
            "description": "ID of the task to update"
        },
        "title": {
            "type": "string",
            "description": "New title for the task (optional)"
        },
        "description": {
            "type": "string",
            "description": "New description for the task (optional)"
        },
        "user_id": {
            "type": "string",
            "description": "ID of the user updating the task (derived from JWT context)"
        }
    }
)