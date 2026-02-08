from typing import Dict, Any
from backend.src.mcp_server.server import mcp_server
from backend.src.services.sync_task_service import SyncTaskService
from backend.db import get_session


def delete_task(task_id: int, user_id: str = None) -> Dict[str, Any]:
    """
    Delete a task safely for the authenticated user
    """
    if not user_id:
        raise ValueError("user_id is required")

    if not task_id:
        raise ValueError("task_id is required")

    # Create a new session for this operation
    with next(get_session()) as db_session:
        task_service = SyncTaskService(db_session)

        # Get the task to verify it exists and belongs to the user
        existing_task = task_service.get_task_by_id(task_id, user_id)

        # Delete the task
        deleted = task_service.delete_task(task_id, user_id)

        if deleted:
            return {
                "task_id": task_id,
                "status": "deleted",
                "title": existing_task.title,
                "message": f"Successfully deleted task '{existing_task.title}'"
            }
        else:
            raise ValueError(f"Failed to delete task with id {task_id}")


# Register the tool with the MCP server
mcp_server.register_tool(
    name="delete_task",
    func=delete_task,
    description="Delete a task safely. Validates ownership.",
    parameters={
        "task_id": {
            "type": "integer",
            "description": "ID of the task to delete"
        },
        "user_id": {
            "type": "string",
            "description": "ID of the user deleting the task (derived from JWT context)"
        }
    }
)