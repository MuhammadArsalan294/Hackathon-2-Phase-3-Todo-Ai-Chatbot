import sys
import os
from pathlib import Path

# Add the backend directory to the Python path to allow imports from models
backend_dir = Path(__file__).parent.parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from typing import List, Optional
from sqlmodel import select, Session
from models.task import Task, TaskCreate, TaskUpdate
from utils.errors import ResourceNotFoundError


class SyncTaskService:
    def __init__(self, session: Session):
        self.session = session

    def create_task(self, task_data: TaskCreate, user_id: str) -> Task:
        """
        Create a new task for the authenticated user
        """
        task = Task(
            title=task_data.title,
            description=task_data.description,
            completed=task_data.completed,
            user_id=user_id
        )

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return task

    def get_tasks_by_user(self, user_id: str) -> List[Task]:
        """
        Get all tasks for the authenticated user
        """
        statement = select(Task).where(Task.user_id == user_id)
        result = self.session.execute(statement)
        tasks = result.scalars().all()

        return tasks

    def get_task_by_id(self, task_id: int, user_id: str) -> Task:
        """
        Get a specific task by ID for the authenticated user
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = self.session.execute(statement)

        task = result.scalar_one_or_none()
        if not task:
            raise ResourceNotFoundError(detail="Task not found or does not belong to user")

        return task

    def update_task(self, task_id: int, task_data: TaskUpdate, user_id: str) -> Task:
        """
        Update a specific task for the authenticated user
        """
        # First get the existing task to check ownership
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = self.session.execute(statement)

        task = result.scalar_one_or_none()
        if not task:
            raise ResourceNotFoundError(detail="Task not found or does not belong to user")

        # Update task fields if provided
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        # Update timestamp
        from datetime import datetime
        task.updated_at = datetime.utcnow()

        self.session.commit()
        self.session.refresh(task)

        return task

    def update_task_completion(self, task_id: int, completed: bool, user_id: str) -> Task:
        """
        Update the completion status of a task for the authenticated user
        """
        # First get the existing task to check ownership
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = self.session.execute(statement)

        task = result.scalar_one_or_none()
        if not task:
            raise ResourceNotFoundError(detail="Task not found or does not belong to user")

        # Update completion status
        task.completed = completed
        from datetime import datetime
        task.updated_at = datetime.utcnow()

        self.session.commit()
        self.session.refresh(task)

        return task

    def delete_task(self, task_id: int, user_id: str) -> bool:
        """
        Delete a specific task for the authenticated user
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = self.session.execute(statement)

        task = result.scalar_one_or_none()
        if not task:
            raise ResourceNotFoundError(detail="Task not found or does not belong to user")

        self.session.delete(task)
        self.session.commit()

        return True