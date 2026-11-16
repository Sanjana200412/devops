# Task Tracker API

A small REST API built with Python, FastAPI, and SQLite. Docker Compose keeps the
database in a named volume so tasks survive container restarts.

## Run with Docker

```sh
docker compose up --build
```

Open the interactive API docs at <http://localhost:8000/docs>.

## Deploy to Google Cloud Run

The GitHub Actions workflow builds the image, pushes it to Artifact Registry,
and deploys it to Cloud Run in `asia-south1` whenever code is pushed to `main`.
The workflow uses Workload Identity Federation and does not require a stored
service-account key. The GCP project and repository identifiers are configured
in the workflow.

```sh
gcloud services enable artifactregistry.googleapis.com run.googleapis.com iamcredentials.googleapis.com sts.googleapis.com \
  --project=project-f4388e1a-a3aa-4cdb-87e
gcloud artifacts repositories create devops \
  --repository-format=docker \
  --location=asia-south1 \
  --project=project-f4388e1a-a3aa-4cdb-87e
```

The GitHub OIDC provider must trust only this repository's `main` branch. The
deployer service account needs Artifact Registry Writer, Cloud Run Admin, and
Service Account User permissions. The deployed service allows unauthenticated
access. Its local SQLite database is ephemeral; use a managed database if task
data must persist.

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

The local database is stored at `data/tasks.db`. Set `DATABASE_PATH` to change it.11
