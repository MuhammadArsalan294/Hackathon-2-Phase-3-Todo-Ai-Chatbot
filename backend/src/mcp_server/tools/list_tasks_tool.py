from typing import Dict, Any, List
from backend.src.mcp_server.server import mcp_server
from backend.src.services.sync_task_service import SyncTaskService
from backend.db import get_session


def list_tasks(status: str = "all", user_id: str = None) -> Dict[str, Any]:
    """
    Return user's tasks filtered by status
    """
    if not user_id:
        raise ValueError("user_id is required")

    # Validate status parameter
    valid_statuses = ["all", "pending", "completed"]
    if status not in valid_statuses:
        status = "all"

    # Create a new session for this operation
    with next(get_session()) as db_session:
        task_service = SyncTaskService(db_session)

        # Get all tasks for the user first
        tasks = task_service.get_tasks_by_user(user_id)

        # Filter based on status if needed
        if status == "pending":
            tasks = [task for task in tasks if not task.completed]
        elif status == "completed":
            tasks = [task for task in tasks if task.completed]

        # Format the tasks for the response
        formatted_tasks = []
        for task in tasks:
            formatted_tasks.append({
                "id": task.id,
                "title": task.title,
                "description": task.description or '',
                "completed": task.completed,
                "created_at": str(task.created_at),
                "updated_at": str(task.updated_at)
            })

        return {
            "tasks": formatted_tasks,
            "count": len(formatted_tasks),
            "status_filter": status,
            "message": f"Found {len(formatted_tasks)} {status} tasks"
        }


# Register the tool with the MCP server
mcp_server.register_tool(
    name="list_tasks",
    func=list_tasks,
    description="Return user's tasks filtered by status (all, pending, completed)",
    parameters={
        "status": {
            "type": "string",
            "description": "Filter tasks by status: 'all', 'pending', or 'completed'",
            "enum": ["all", "pending", "completed"]
        },
        "user_id": {
            "type": "string",
            "description": "ID of the user whose tasks to list (derived from JWT context)"
        }
    }
)