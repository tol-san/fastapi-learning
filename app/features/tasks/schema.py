from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.features.tasks.model import TaskStatus


class TaskCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
    )

    description: str | None = None

    status: TaskStatus = TaskStatus.TODO

    due_date: datetime | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    description: str | None = None

    status: TaskStatus | None = None

    due_date: datetime | None = None


class TaskResponse(BaseModel):
    id: int

    title: str

    description: str | None

    status: TaskStatus

    due_date: datetime | None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )