from typing import List, Optional
from sqlmodel import select, update, delete
from models.task import Task, TaskCreate, TaskUpdate
from utils.errors import ResourceNotFoundError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(self, task_data: TaskCreate, user_id: str) -> Task:
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
        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def get_tasks_by_user(self, user_id: str) -> List[Task]:
        """
        Get all tasks for the authenticated user
        """
        statement = select(Task).where(Task.user_id == user_id)
        result = await self.session.execute(statement)
        tasks = result.scalars().all()

        return tasks

    async def get_task_by_id(self, task_id: int, user_id: str) -> Task:
        """
        Get a specific task by ID for the authenticated user
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await self.session.execute(statement)

        try:
            task = result.scalar_one()
            return task
        except NoResultFound:
            raise ResourceNotFoundError(detail="Task not found or does not belong to user")

    async def update_task(self, task_id: int, task_data: TaskUpdate, user_id: str) -> Task:
        """
        Update a specific task for the authenticated user
        """
        # First get the existing task to check ownership
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await self.session.execute(statement)

        try:
            task = result.scalar_one()
        except NoResultFound:
            raise ResourceNotFoundError(detail="Task not found or does not belong to user")

        # Update task fields if provided
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        # Update timestamp
        from datetime import datetime
        task.updated_at = datetime.utcnow()

        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def update_task_completion(self, task_id: int, completed: bool, user_id: str) -> Task:
        """
        Update the completion status of a task for the authenticated user
        """
        # First get the existing task to check ownership
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await self.session.execute(statement)

        try:
            task = result.scalar_one()
        except NoResultFound:
            raise ResourceNotFoundError(detail="Task not found or does not belong to user")

        # Update completion status
        task.completed = completed
        from datetime import datetime
        task.updated_at = datetime.utcnow()

        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def delete_task(self, task_id: int, user_id: str) -> bool:
        """
        Delete a specific task for the authenticated user
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await self.session.execute(statement)

        try:
            task = result.scalar_one()
        except NoResultFound:
            raise ResourceNotFoundError(detail="Task not found or does not belong to user")

        await self.session.delete(task)
        await self.session.commit()

        return True