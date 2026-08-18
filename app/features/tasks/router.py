from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.features.tasks.schema import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)
from app.features.tasks.service import TaskService


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


DbSession = Annotated[
    AsyncSession,
    Depends(get_db),
]


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    data: TaskCreate,
    db: DbSession,
):
    return await TaskService.create_task(
        db=db,
        data=data,
    )


@router.get(
    "",
    response_model=list[TaskResponse],
)
async def get_tasks(
    db: DbSession,
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
):
    return await TaskService.get_tasks(
        db=db,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
async def get_task(
    task_id: int,
    db: DbSession,
):
    return await TaskService.get_task(
        db=db,
        task_id=task_id,
    )


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
)
async def update_task(
    task_id: int,
    data: TaskUpdate,
    db: DbSession,
):
    return await TaskService.update_task(
        db=db,
        task_id=task_id,
        data=data,
    )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: int,
    db: DbSession,
):
    await TaskService.delete_task(
        db=db,
        task_id=task_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )