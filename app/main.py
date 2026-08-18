from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class Task(BaseModel):
    title: str
    description: str
    completed: bool = False

app = FastAPI()

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id != 1:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "task_id": task_id,
        "title": "Learn FastAPI",
    }

@app.post("/tasks")
def create_task(task: Task):
    return task

@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}

@app.get("/users")
def get_users():
    return {"message": "Get users"}

@app.post("/users")
def create_user():
    return {"message": "Create user"}


@app.put("/users/{id}")
def update_user(id: int):
    return {"message": f"Update user with id {id}"}

@app.delete("/users/{id}")
def delete_user(id: int):
    return {"message": f"Delete user with id {id}"}


@app.get("/tasks")
def get_tasks(limit: int = 10):
    return {"limit": limit}


