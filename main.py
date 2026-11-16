import os
import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

DATABASE_PATH = Path(os.getenv("DATABASE_PATH", "data/tasks.db"))

app = FastAPI(title="Task Tracker API", version="1.0.0")


class TaskCreate(BaseModel):
    title: str


class Task(BaseModel):
    id: int
    title: str
    completed: bool


def connect() -> sqlite3.Connection:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0
            )
            """
        )


init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[dict[str, object]]:
    with connect() as connection:
        rows = connection.execute(
            "SELECT id, title, completed FROM tasks ORDER BY id"
        ).fetchall()
    return [
        {"id": row["id"], "title": row["title"], "completed": bool(row["completed"])}
        for row in rows
    ]


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate) -> dict[str, object]:
    title = task.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title must not be empty")

    with connect() as connection:
        cursor = connection.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        row = connection.execute(
            "SELECT id, title, completed FROM tasks WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
    return {"id": row["id"], "title": row["title"], "completed": bool(row["completed"])}


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int) -> None:
    with connect() as connection:
        cursor = connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found")
