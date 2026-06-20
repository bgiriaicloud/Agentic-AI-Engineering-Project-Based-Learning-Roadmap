# Project 3: LLMOps & AI DevOps
*Duration: 4 Weeks | Focus: MLOps & Deployment*

## 📖 Project Brief
Students will containerize a model inference API (built with FastAPI and a lightweight HuggingFace sentiment pipeline) using Docker, write Kubernetes deployment configuration files, configure automated monitoring endpoints with Prometheus and Grafana, and design a deployment architecture suitable for hosting AI microservices.

---

## 🎯 Learning Objectives
- Containerize Python applications with multi-stage `Dockerfiles` optimizing for size and caching.
- Understand CPU/GPU resource allocation constraints in container execution.
- Create Kubernetes Pod, Deployment, and Service manifests with health checks (readiness/liveness probes).
- Integrate custom metrics instrumentation (FastAPI + Prometheus custom metrics).
- Monitor API request latency, queue lengths, and container resource limits.
- Understand canary and rolling update deployment strategies.

---

## 🏗️ Project Architecture Diagram

```
+------------------------------------------------------------------------+
|                      LLMOPS WORKFLOW ARCHITECTURE                      |
+------------------------------------------------------------------------+
|                                                                        |
|      [Local Python Code]               [HuggingFace Model Weights]     |
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

Follow these steps to containerize, deploy, and monitor the Inference API:

1. **Service Inception:** Develop the FastAPI application in `src/main.py` with standard model input validation models using Pydantic.
2. **HuggingFace Pipeline Setup:** Incorporate a sentiment analysis pipeline loader inside `src/main.py`. Build a mock fallback classifier to handle CPU-only offline dry-runs.
3. **Instrument Metrics:** Add Prometheus metric tracking variables (Counter for requests, Histogram for inference durations) and construct the `/metrics` scraper endpoint in `src/main.py`.
4. **Health Check Probes:** Expose standard `/` health checking targets and a `/ready` path that checks if the model weights are loaded and ready.
5. **Optimize Docker Layers:** Write the multi-stage `Dockerfile` to cache pip dependencies and isolate system build utilities from the runtime image.
6. **Local Container Verification:** Build the Docker image locally and execute it with port forwarding to test API queries manually.
7. **Local Cluster Activation:** Install and launch Minikube (`minikube start`) and map your terminal shell to Minikube's internal Docker registry.
8. **Draft K8s Deployment Manifest:** Write `deployment.yaml` defining 2 replicas, resource allocations (250m CPU requests, 1Gi Memory limits), and readiness/liveness timeout specifications.
9. **Draft K8s Service Manifest:** Write `service.yaml` specifying a NodePort service mapping port 8000 to port 30080 on the host VM.
10. **Deploy and Expose:** Apply your manifests using `kubectl apply` commands and retrieve the NodePort access address from Minikube.
11. **Configure Monitoring Scrapers:** Create `prometheus.yml` containing target scrapers that pull telemetry metrics from your running FastAPI pod endpoints.
12. **Test Scaling Resilience:** Simulate replica failures by deleting a pod and watch Kubernetes self-healing features spin up replacement instances.

---

## 📅 Week-by-Week Deliverables

### Week 1: Docker Containerization
- Build a FastAPI service that runs a lightweight text sentiment classification pipeline (HuggingFace Transformers).
- Implement a Dockerfile optimizing layers for model caching.
- **Deliverable:** `Dockerfile` and local container running at port `8000`.

### Week 2: Kubernetes Configuration
- Install Minikube/Kubectl locally.
- Write Kubernetes `deployment.yaml` and `service.yaml` manifests.
- Specify request and limit thresholds for CPU and Memory.
- **Deliverable:** Successful deployment of the API pod on Minikube.

### Week 3: Metrics Instrumentation
- Implement custom `/metrics` endpoint using `prometheus_client`.
- Export custom metrics: inference request count, prediction inference latency (histogram), and active request count.
- Configure `prometheus.yml` scrapers to poll target pods.
- **Deliverable:** `prometheus.yml` configuration and active scraper metrics logs.

### Week 4: Deployment Validation & Strategies
- Test rolling update changes using Kubernetes rollout commands.
- Simulate container failures (e.g. out-of-memory or liveness timeout) and verify automatic pod restarts.
- **Deliverable:** Completed documentation on debugging container lifecycles.

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
| **Dockerfile Optimization** | 20% | Correct use of multi-stage structures, base images, and layers optimizing model weight caching. |
| **Kubernetes Declarations** | 30% | Correct resources allocations (limits vs requests), health checks, and service configurations. |
| **Prometheus Instrumentation** | 30% | Accurate setup of histograms and counters tracking API throughput and performance. |
| **Rollouts & Failure Resilience** | 10% | Correct application of deployment rolling updates and handling pod errors. |
| **Code Structure & Readme** | 10% | Clean formatting and description of steps. |

---

## 🛠️ Troubleshooting & Tips
- **ImagePullBackOff:** If Minikube cannot pull your image, ensure you run `eval $(minikube docker-env)` before building the image, or set `imagePullPolicy: Replace/Never` inside `deployment.yaml`.
- **Memory Limits:** Sentiment analysis pipeline on HuggingFace can draw more memory than typical microservices. If your container gets killed immediately, increase K8s resource requests limit in `deployment.yaml`.
