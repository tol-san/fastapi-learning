from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.tasks.model import Task
from app.features.tasks.repository import TaskRepository
from app.features.tasks.schema import TaskCreate, TaskUpdate


class TaskService:

    @staticmethod
    async def create_task(
        db: AsyncSession,
        data: TaskCreate,
    ) -> Task:
        return await TaskRepository.create(
            db=db,
            data=data,
        )

    @staticmethod
    async def get_tasks(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        return await TaskRepository.get_all(
            db=db,
            skip=skip,
            limit=limit,
        )

    @staticmethod
    async def get_task(
        db: AsyncSession,
        task_id: int,
    ) -> Task:
        task = await TaskRepository.get_by_id(
            db=db,
            task_id=task_id,
        )

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        return task

    @staticmethod
    async def update_task(
        db: AsyncSession,
        task_id: int,
        data: TaskUpdate,
    ) -> Task:
        task = await TaskService.get_task(
            db=db,
            task_id=task_id,
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if update_data.get("title") is None and "title" in update_data:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Task title cannot be null",
            )

        if update_data.get("status") is None and "status" in update_data:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Task status cannot be null",
            )

        return await TaskRepository.update(
            db=db,
            task=task,
            data=data,
        )

    @staticmethod
    async def delete_task(
        db: AsyncSession,
        task_id: int,
    ) -> None:
        task = await TaskService.get_task(
            db=db,
            task_id=task_id,
        )

        await TaskRepository.delete(
            db=db,
            task=task,
        )