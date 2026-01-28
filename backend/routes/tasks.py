from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_async_session
from dependencies.auth import get_current_user
from services.task_service import TaskService
from models.task import Task, TaskCreate, TaskUpdate
from schemas.task import TaskResponse, TaskCompletionUpdate
from utils.errors import ResourceNotFoundError


router = APIRouter(tags=["tasks"])


@router.get("", response_model=List[TaskResponse])
async def get_tasks(
    current_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get all tasks for the authenticated user
    """
    task_service = TaskService(session)
    tasks = await task_service.get_tasks_by_user(current_user_id)

    return tasks


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_create: TaskCreate,
    current_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new task for the authenticated user
    """
    task_service = TaskService(session)
    task = await task_service.create_task(task_create, current_user_id)

    return task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get a specific task by ID for the authenticated user
    """
    task_service = TaskService(session)
    task = await task_service.get_task_by_id(task_id, current_user_id)

    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Update a specific task for the authenticated user
    """
    task_service = TaskService(session)
    task = await task_service.update_task(task_id, task_update, current_user_id)

    return task


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def update_task_completion(
    task_id: int,
    completion_update: TaskCompletionUpdate,
    current_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Update the completion status of a task for the authenticated user
    """
    task_service = TaskService(session)
    task = await task_service.update_task_completion(task_id, completion_update.completed, current_user_id)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Delete a specific task for the authenticated user
    """
    task_service = TaskService(session)
    await task_service.delete_task(task_id, current_user_id)

    # 204 No Content should return nothing