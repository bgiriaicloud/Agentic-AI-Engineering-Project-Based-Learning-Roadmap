# Project 3: LLMOps & AI DevOps
*Duration: 4 Weeks | Focus: MLOps & Deployment*

## 📖 Project Brief
Students will containerize a model inference API (built with FastAPI serving a **Google Antigravity SDK (ADK)** Agent) using Docker, write Kubernetes deployment configuration files, configure automated monitoring endpoints with Prometheus and Grafana, and design a deployment architecture suitable for hosting AI microservices.

---

## 🎯 Learning Objectives
- Containerize Python applications with multi-stage `Dockerfiles` optimizing for size and caching.
- Serve a stateful/async Agent via FastAPI.
- Create Kubernetes Pod, Deployment, and Service manifests with health checks (readiness/liveness probes).
- Integrate custom telemetry metrics (FastAPI + Prometheus custom metrics).
- Monitor Agent request latency and error rates.
- Understand canary and rolling update deployment strategies.

---

## 🏗️ Project Architecture Diagram

```
+------------------------------------------------------------------------+
|                      LLMOPS WORKFLOW ARCHITECTURE                      |
+------------------------------------------------------------------------+
|                                                                        |
|      [Local Python Code]               [GCP Gemini Model API]          |
|              │                                      │                  |
|              ▼ (Build Docker Container Layers)      │                  |
|      [Docker Image (ai-inference-app)] <────────────+                  |
|              │                                                         |
|              ▼ (kubectl apply configuration manifests)                 |
|     +──────────────────────────────────────────────────────────+       |
|     │                 MINIKUBE KUBERNETES CLUSTER              │       |
|     │                                                          │       |
|     │   [LoadBalancer / NodePort Service] (Port: 30080)        │       |
|     │               │                                          │       |
|     │               ▼ (Route requests to target pods)          │       |
|     │   +──────────────────────────────────────────────────+   │       |
|     │   │     K8s Deployment (Replicas: 2)                 │   │       |
|     │   │  [Inference App Pod 1]    [Inference App Pod 2]  │   │       |
|     │   │   FastAPI Port 8000        FastAPI Port 8000     │   │       |
|     │   │     /ready Probe             /ready Probe        │   │       |
|     │   +───────┬────────────────────────┬─────────────────+   │       |
|     +───────────┼────────────────────────┼─────────────────────+       |
|                 │ (Poll metrics endpoint)│                             |
|                 ▼                        ▼                             |
|         [Prometheus Server Scraping Endpoint (/metrics)]               |
|                 │                                                      |
|                 ▼ (Telemetry Dashboard Logs)                           |
|         [Grafana Analytics Dashboard]                                  |
|                                                                        |
+------------------------------------------------------------------------+
```

---

## 🚦 Step-by-Step Implementation Guide

Follow these steps to containerize, deploy, and monitor the Agent API:

1. **Service Inception:** Develop the FastAPI application in `src/main.py` with standard model input validation models using Pydantic.
2. **Setup Async ADK Agent:** Incorporate an async chat execute method in `src/main.py` that handles `Agent` initialization using `LocalAgentConfig`.
3. **Instrument Telemetry Metrics:** Add Prometheus metric tracking variables (Counter for agent requests, Histogram for model durations) and construct the `/metrics` scraper endpoint in `src/main.py`.
4. **Health Check Probes:** Expose standard `/` health checking targets and a `/ready` path that checks if the service is ready.
5. **Optimize Docker Layers:** Write the multi-stage `Dockerfile` to cache pip dependencies and isolate system build utilities from the runtime image.
6. **Local Container Verification:** Build the Docker image locally and execute it with port forwarding to test API queries manually.
7. **Local Cluster Activation:** Install and launch Minikube (`minikube start`) and map your terminal shell to Minikube's internal Docker registry.
8. **Draft K8s Deployment Manifest:** Write `deployment.yaml` defining 2 replicas, resource allocations (250m CPU requests, 1Gi Memory limits), and readiness/liveness timeout specifications.
9. **Draft K8s Service Manifest:** Write `service.yaml` specifying a NodePort service mapping port 8000 to port 30080 on the host VM.
10. **Deploy and Expose:** Apply your manifests using `kubectl apply` commands and retrieve the NodePort access address from Minikube.
11. **Configure Monitoring Scrapers:** Create `prometheus.yml` containing scraper settings targeting your FastAPI metrics endpoint.
12. **Verify Telemetry Output:** Hit the `http://localhost:8000/metrics` target and verify custom counters and histograms are logged correctly.

---

## 📁 Repository Structure
```
P3-llmops-devops/
├── README.md
├── requirements.txt
├── Dockerfile
├── deployment.yaml
├── service.yaml
├── prometheus.yml
└── src/
    └── main.py
```

---

## 🚀 Setup & Execution

### 1. Run the FastAPI App locally
```bash
pip install -r requirements.txt
python src/main.py
```
Check API documentation at `http://localhost:8000/docs`.

### 2. Build and Run Container
```bash
# Build Docker image
docker build -t ai-inference-app:latest .

# Run Docker container
docker run -p 8000:8000 ai-inference-app:latest
```

### 3. Deploy to Kubernetes (Minikube)
Ensure Minikube is started:
```bash
minikube start

# Switch docker environment to minikube daemon
eval $(minikube docker-env)

# Build image inside minikube environment
docker build -t ai-inference-app:latest .

# Apply manifests
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Expose service
minikube service ai-inference-app-service
```

---

## 📊 Grading Rubric (100 Points)

| Criteria | Weight | Description |
| :--- | :--- | :--- |
| **Dockerfile Optimization** | 20% | Correct use of multi-stage structures, base images, and layers optimizing dependencies. |
| **Kubernetes Declarations** | 30% | Correct resources allocations (limits vs requests), health checks, and service configurations. |
| **Prometheus Telemetry** | 30% | Accurate setup of histograms and counters tracking Agent chat latency and request rates. |
| **Rollouts & Failure Resilience** | 10% | Correct application of deployment rolling updates and handling pod errors. |
| **Code Structure & Readme** | 10% | Clean formatting and description of steps. |
