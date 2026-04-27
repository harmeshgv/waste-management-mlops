# Waste Management MLOps

An end-to-end waste classification and task management project built with FastAPI, PyTorch, PostgreSQL, Docker, Kubernetes, and a lightweight frontend dashboard.

The app can:
- classify uploaded waste images with an EfficientNet-based model
- store waste reports as pending cleanup tasks
- prioritize and deduplicate tasks by severity and location
- generate a simple route plan for collection
- mark completed tasks from the dashboard

## Tech Stack

- Python
- FastAPI
- PyTorch
- PostgreSQL
- Docker and Docker Compose
- Kubernetes manifests
- Pytest
- GitHub Actions
- Optional Splunk logging

## Project Structure

```text
waste-management-mlops/
├── backend/
│   ├── db/
│   ├── models/
│   ├── utils/
│   ├── main.py
│   └── requirements.txt
├── model/
│   ├── class_labels.json
│   └── *.pth
├── tests/
├── .github/workflows/
├── docker-compose.yml
├── Dockerfile
├── index.html
├── k8s/
├── requirements-dev.txt
└── readme.md
```

## Features

- Image classification endpoint for waste category prediction
- Auto-persistence of predicted waste reports into the database
- City and locality mapping for task coordinates
- Severity-based task ordering
- Greedy route generation for pending tasks
- Single-page dashboard for all API endpoints
- Automated tests for API behavior and route logic
- GitHub Actions workflow for test execution

## API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/` | Serves the frontend dashboard |
| `GET` | `/health` | Health check |
| `POST` | `/predict` | Upload image and create a task |
| `GET` | `/tasks?city=<city>` | List pending tasks for a city |
| `GET` | `/route?city=<city>` | Generate an ordered route |
| `POST` | `/complete?task_id=<id>` | Mark a task as completed |

## Run Locally

### Option 1: Python virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
export DATABASE_URL=postgresql://<user>:<password>@<host>:5432/<database_name>
uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload
```

Use this mode if you already have a PostgreSQL instance running and want to point the app at it manually.

Open:

- Dashboard: `http://localhost:8001`
- API docs: `http://localhost:8001/docs`

### Option 2: Docker Compose

```bash
docker compose up --build
```

Open:

- Dashboard: `http://localhost:8001`

## Running Tests

Install test dependencies:

```bash
pip install -r requirements-dev.txt
```

Run the suite:

```bash
python3 -m pytest -q
```

Current coverage includes:
- health endpoint
- predict endpoint
- tasks endpoint
- route endpoint
- complete endpoint
- distance, deduplicate, and route helper logic

## CI

GitHub Actions is configured in:

```text
.github/workflows/run_tests.yml
```

The workflow:
- runs on pushes and pull requests
- sets up Python 3.12
- installs test dependencies
- runs `pytest`

## Docker Notes

The backend container:
- serves the FastAPI app on port `8001`
- serves the frontend dashboard from the same origin
- loads model files from the `model/` directory

The Compose stack includes:
- `db` for PostgreSQL
- `backend` for the FastAPI application

## Kubernetes Notes

Kubernetes manifests are available under `k8s/`.

Before using the Kubernetes deployment:
- update the Splunk token placeholder in `k8s/backend-deployment.yaml`
- ensure the backend image exists in the environment where your cluster can access it

## Splunk Logging

Splunk logging is optional.

The app reads these environment variables if you want to enable it:

- `SPLUNK_HEC_HOST`
- `SPLUNK_HEC_PORT`
- `SPLUNK_HEC_TOKEN`

If `SPLUNK_HEC_TOKEN` is not set, Splunk logging stays disabled.

## Notes Before Pushing to GitHub

- local logs, virtual environments, cache folders, and generated test files are ignored
- Docker build context is trimmed with `.dockerignore`
- the Kubernetes Splunk token has been replaced with a placeholder
- tests are ready to run in CI

## Future Improvements

- add authentication for admin task actions
- move secrets to environment files or Kubernetes secrets
- improve route optimization beyond the current greedy strategy
- add coverage reporting to CI
- deploy with a production-ready container registry and cluster
