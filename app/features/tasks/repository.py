from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.tasks.model import Task
from app.features.tasks.schema import TaskCreate, TaskUpdate


class TaskRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        data: TaskCreate,
    ) -> Task:
        task = Task(**data.model_dump())

        db.add(task)

        await db.commit()
        await db.refresh(task)

        return task

    @staticmethod
    async def get_all(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        statement = (
            select(Task)
            .order_by(Task.id.desc())
            .offset(skip)
            .limit(limit)
        )

        result = await db.execute(statement)

        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        task_id: int,
    ) -> Task | None:
        statement = select(Task).where(
            Task.id == task_id
        )

        result = await db.execute(statement)

        return result.scalar_one_or_none()

    @staticmethod
    async def update(
        db: AsyncSession,
        task: Task,
        data: TaskUpdate,
    ) -> Task:
        update_data = data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(task, field, value)

        await db.commit()
        await db.refresh(task)

        return task

    @staticmethod
    async def delete(
        db: AsyncSession,
        task: Task,
    ) -> None:
        await db.delete(task)
        await db.commit()