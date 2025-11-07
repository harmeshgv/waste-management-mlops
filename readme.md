# Waste Management ML + DevOps Pipeline

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68%2B-green)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue)](https://docker.com)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Minikube-orange)](https://minikube.sigs.k8s.io)
[![Splunk](https://img.shields.io/badge/Monitoring-Splunk-yellow)](https://splunk.com)

## Overview

This project integrates **Machine Learning (ML)** and **DevOps** to create an end-to-end automated system for waste classification and monitoring. It uses:

* **FastAPI** for backend API serving
* **Docker & Kubernetes (Minikube)** for containerization and orchestration
* **Splunk** for real-time centralized logging and monitoring
* **CI/CD pipeline integration (DevOps)** to ensure smooth deployment and observability

## ML + DevOps Workflow

1. **ML Model (PyTorch)** -> Predicts waste category from input images
2. **FastAPI Backend** -> Serves the model via REST API
3. **Docker + Minikube** -> Manages containerized deployments
4. **Splunk** -> Collects and visualizes real-time logs
5. **DevOps** -> Automates builds, logs, and monitoring

## Run the Project Locally

### 1. Using Uvicorn (Development Mode)

Make sure you are in your virtual environment and inside the project directory.

```bash
(venv) user@host:~/Documents/waste-management-ml$ uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload
```

This will start the FastAPI server on:
**http://localhost:8001**

### 2. Using Docker

Build and run the containerized backend:

```bash
# Build Docker image
docker build -t waste-backend:latest .

# Run container (map internal port 8001 to host port 8001)
docker run -d -p 8001:8001 waste-backend:latest
```

Access API at:
**http://localhost:8001**

## 3. Setup Splunk for Centralized Logging

Clone the Splunk setup repository parallel to this project or anywhere you prefer:

```bash
git clone https://github.com/harmeshgv/splunk-lab.git
cd splunk-lab
chmod +x splunk-setup.sh
./splunk-setup.sh
```

Wait for setup to complete (around 1-2 minutes).
Then, open Splunk in your browser:
**http://localhost:8000**

**Login credentials:**
```
Username: admin
Password: admin12345
```

### Configure Splunk HTTP Event Collector (HEC)

1. In Splunk Web, go to **Settings -> Data Inputs -> HTTP Event Collector -> New Token**
2. **Set Name:** `waste-ml-logs`
3. **Select Index:** `main`
4. **Copy the Generated Token** (e.g. `d81ae29d-1b40-43f8-9314-cf3136932ce2`)

### Update Splunk Config in Backend Deployment (for Kubernetes)

In `k8s/backend-deployment.yaml`, update:

```yaml
- name: SPLUNK_HEC_URL
  value: "http://localhost:8088"
- name: SPLUNK_HEC_TOKEN
  value: "d81ae29d-1b40-43f8-9314-cf3136932ce2"
```

(Only replace the token value with yours.)

## 4. Deploy on Minikube

### Step 1: Start Minikube

```bash
minikube start
```

### Step 2: Verify Docker Image

Make sure the image name in your YAML (`waste-backend:latest`) matches the one built locally.
If needed, build it inside Minikube's Docker environment:

```bash
eval $(minikube docker-env)
docker build -t waste-backend:latest .
```

### Step 3: Apply Deployment

```bash
kubectl apply -f k8s/backend-deployment.yaml
```

### Step 4: Check Pods & Services

```bash
kubectl get pods
kubectl get svc
```

### Step 5: Access Minikube Dashboard

```bash
minikube dashboard
```

This will open the Kubernetes dashboard in your default browser where you can monitor your deployments, pods, and services.

## 5. View Logs in Splunk Dashboard

Once the backend starts sending logs to Splunk, open:
**http://localhost:8000**

Go to **Search & Reporting** and type:

```
source=*
```

You'll see real-time logs from your FastAPI backend (like prediction logs, request status, etc.).

### Example Log Query for ML Predictions

This query extracts ML prediction details from logs and visualizes counts per class:

```spl
index=* "Prediction successful:"
| rex field=_raw "Prediction successful: (?<predicted_class>[A-Za-z_]+)"
| stats count by predicted_class
| sort - count
```

This helps track which waste categories are most commonly predicted — directly linking **ML insights** with **DevOps observability**.

## Integration Summary

| Component                | Description            | Purpose                           |
| ------------------------ | ---------------------- | --------------------------------- |
| ML Model                 | EfficientNet / PyTorch | Classifies waste images           |
| FastAPI                  | Backend API            | Serves prediction results         |
| Docker                   | Containerization       | Portable environment setup        |
| Kubernetes (Minikube)    | Orchestration          | Scales and manages containers     |
| Splunk                   | Logging & Monitoring   | Tracks and visualizes ML logs     |
| DevOps                   | CI/CD + Observability  | Automates deployment & monitoring |

## Example Use Case

* Upload image of waste via API -> Backend runs ML model -> Prediction logged in Splunk.
* Splunk visualizes "Most Predicted Waste Types" dashboard in real-time.
* DevOps ensures continuous deployment with versioned ML models.

## Dashboard Access

### Minikube Dashboard
```bash
minikube dashboard
```
Access the Kubernetes dashboard to monitor:
- Pod status and resource usage
- Service endpoints
- Deployment history
- Log streams from containers

### Splunk Dashboard
**http://localhost:8000**
Access the Splunk dashboard to monitor:
- Real-time application logs
- ML prediction analytics
- System performance metrics
- Custom visualizations and reports

## Cleanup (Optional)

To remove Splunk setup:

```bash
cd splunk-lab
./splunk-cleanup.sh
```

To stop Minikube:

```bash
minikube stop
```



