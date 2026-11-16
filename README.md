# Task Tracker API

A small REST API built with Python, FastAPI, and SQLite. Docker Compose keeps the
database in a named volume so tasks survive container restarts.

## Run with Docker

```sh
docker compose up --build
```

Open the interactive API docs at <http://localhost:8000/docs>.

## Endpoints

- `GET /health` — service status
- `GET /tasks` — list tasks
- `POST /tasks` — create a task, with JSON such as `{"title":"Try Docker"}`
- `DELETE /tasks/{task_id}` — delete a task

## Run locally

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The local database is stored at `data/tasks.db`. Set `DATABASE_PATH` to change it.
