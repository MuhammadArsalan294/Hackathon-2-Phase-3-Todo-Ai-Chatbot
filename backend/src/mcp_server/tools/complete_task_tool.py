from typing import Dict, Any
from backend.src.mcp_server.server import mcp_server
from backend.src.services.sync_task_service import SyncTaskService
from backend.models.task import TaskUpdate
from backend.db import get_session


def complete_task(task_id: int, user_id: str = None) -> Dict[str, Any]:
    """
    Mark a task as completed for the authenticated user
    """
    if not user_id:
        raise ValueError("user_id is required")

    if not task_id:
        raise ValueError("task_id is required")

    # Create a new session for this operation
    with next(get_session()) as db_session:
        task_service = SyncTaskService(db_session)

        # Update the task to mark it as completed
        update_data = TaskUpdate(completed=True)
        updated_task = task_service.update_task_completion(task_id, True, user_id)

        return {
            "task_id": updated_task.id,
            "status": "completed",
            "title": updated_task.title,
            "message": f"Successfully marked task '{updated_task.title}' as completed"
        }


# Register the tool with the MCP server
mcp_server.register_tool(
    name="complete_task",
    func=complete_task,
    description="Mark a task as completed. Validates ownership.",
    parameters={
        "task_id": {
            "type": "integer",
            "description": "ID of the task to mark as completed"
        },
        "user_id": {
            "type": "string",
            "description": "ID of the user completing the task (derived from JWT context)"
        }
    }
)