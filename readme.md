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

This repository now includes a Kubernetes-only Minikube setup with:
- a dedicated `waste-mlops` namespace
- in-cluster PostgreSQL with persistent storage
- a FastAPI backend Deployment
- a backend ClusterIP Service
- an Ingress for browser access

Manifest set:

```text
k8s/
├── namespace.yaml
├── postgres-secret.yaml
├── postgres-configmap.yaml
├── postgres-service.yaml
├── postgres-statefulset.yaml
├── backend-configmap.yaml
├── backend-secret.yaml
├── backend-deployment.yaml
├── backend-service.yaml
├── ingress.yaml
├── fluent-bit-secret.yaml
├── fluent-bit-configmap.yaml
├── fluent-bit-rbac.yaml
└── fluent-bit-daemonset.yaml
```

### Minikube Setup

1. Start Minikube:

```bash
minikube start
```

2. Enable ingress:

```bash
minikube addons enable ingress
```

3. Build the backend image inside Minikube:

```bash
eval $(minikube docker-env)
docker build -t waste-backend:minikube .
```

4. Apply the namespace first:

```bash
kubectl apply -f k8s/namespace.yaml
```

5. Before applying secret manifests, replace placeholder values in:

```text
k8s/postgres-secret.yaml
k8s/backend-secret.yaml
k8s/fluent-bit-secret.yaml
```

6. Apply the remaining manifests:

```bash
kubectl apply -f k8s/postgres-secret.yaml
kubectl apply -f k8s/postgres-configmap.yaml
kubectl apply -f k8s/postgres-service.yaml
kubectl apply -f k8s/postgres-statefulset.yaml
kubectl apply -f k8s/backend-configmap.yaml
kubectl apply -f k8s/backend-secret.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/ingress.yaml
```

Optional Splunk logging setup:

```bash
kubectl apply -f k8s/fluent-bit-secret.yaml
kubectl apply -f k8s/fluent-bit-configmap.yaml
kubectl apply -f k8s/fluent-bit-rbac.yaml
kubectl apply -f k8s/fluent-bit-daemonset.yaml
```

7. Wait for resources:

```bash
kubectl get pods -n waste-mlops
kubectl get pvc -n waste-mlops
kubectl get ingress -n waste-mlops
```

8. Get the Minikube IP:

```bash
minikube ip
```

9. Add this to your `/etc/hosts` file:

```text
<MINIKUBE_IP> waste.local
```

10. Open the app:

```text
http://waste.local
```

### What Each Kubernetes Piece Does

- `namespace.yaml`: keeps the whole app isolated under `waste-mlops`
- `postgres-*`: runs PostgreSQL inside the cluster and stores task data persistently
- `backend-*`: runs the FastAPI app and serves the frontend dashboard
- `ingress.yaml`: exposes one clean browser URL for both frontend and API

### Kubernetes Verification

Health checks:

```bash
kubectl get all -n waste-mlops
kubectl get pvc -n waste-mlops
kubectl describe ingress waste-backend-ingress -n waste-mlops
```

Backend checks:

```bash
kubectl logs deployment/waste-backend -n waste-mlops
curl http://waste.local/health
```

Splunk logging checks:

```bash
kubectl get pods -n waste-mlops -l app.kubernetes.io/name=fluent-bit
kubectl logs -n waste-mlops -l app.kubernetes.io/name=fluent-bit
```

If Splunk is running on your host machine, Fluent Bit forwards logs to:

```text
http://host.minikube.internal:8088
```

In Splunk Web, search:

```text
index=main
```

Useful searches:

```text
index=main kubernetes
index=main waste-backend
index=main postgres
```

Persistence checks:

```bash
kubectl rollout restart deployment/waste-backend -n waste-mlops
kubectl rollout restart statefulset/postgres -n waste-mlops
```

After restart, previously created tasks should still be present because PostgreSQL uses a PVC.

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
- Kubernetes secret manifests contain placeholders and should be filled locally before deployment
- tests are ready to run in CI

## Future Improvements

- add authentication for admin task actions
- move secrets to environment files or Kubernetes secrets
- improve route optimization beyond the current greedy strategy
- add coverage reporting to CI
- deploy with a production-ready container registry and cluster
