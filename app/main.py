from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.features.tasks.router import router as task_router

# Important:
# Import models so SQLAlchemy knows about them
from app.features.tasks.model import Task  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(
            Base.metadata.create_all
        )

    yield

    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)


app.include_router(
    task_router,
    prefix="/api/v1",
)


@app.get("/")
async def root():
    return {
        "message": "Task Management API"
    }