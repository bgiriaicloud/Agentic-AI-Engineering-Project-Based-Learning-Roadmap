# 🎯 Agentic AI Engineering Project-Based Learning Roadmap
*Created by Biswanath Giri*

Welcome to the **Agentic AI Engineering Project-Based Learning (PBL) Roadmap**. This curriculum is designed to guide college students (3rd/4th year undergraduate or graduate level) through the implementation of real-world agentic systems using the **Google Antigravity SDK (ADK)** and the **GCP Agentic AI Ecosystem**.

Rather than working on simple minimum viable products, students will build components of an **Enterprise-Grade Agentic AI Platform**.

---

## 📋 Course Curriculum Overview

| Project | Project Name | Primary Focus | Key Technologies | Duration |
| :--- | :--- | :--- | :--- | :--- |
| **P1** | [Enterprise RAG Assistant](file:///Users/biswanathgiri/Desktop/project-based-agentic-ai-learning/P1-enterprise-rag/README.md) | Retrieval-Augmented Generation | google-antigravity (ADK), Streamlit, ChromaDB, HuggingFace, Gemini | 4 Weeks |
| **P2** | [Multi-Agent AI System](file:///Users/biswanathgiri/Desktop/project-based-agentic-ai-learning/P2-multi-agent-system/README.md) | Agentic AI & Orchestration | google-antigravity (ADK) Subagents, ToolContext state management, Gemini | 4 Weeks |
| **P3** | [LLMOps & AI DevOps](file:///Users/biswanathgiri/Desktop/project-based-agentic-ai-learning/P3-llmops-devops/README.md) | MLOps & Deployment | google-antigravity (ADK), FastAPI, Docker, Kubernetes, Prometheus, Grafana | 4 Weeks |
| **P4** | [AI Evaluation Platform](file:///Users/biswanathgiri/Desktop/project-based-agentic-ai-learning/P4-ai-evaluation/README.md) | Quality Assurance & Testing | DeepEval, RAGAS, google-antigravity (ADK), Streamlit | 4 Weeks |
| **P5** | [Fine-Tuning Pipeline](file:///Users/biswanathgiri/Desktop/project-based-agentic-ai-learning/P5-fine-tuning-pipeline/README.md) | Model Optimization | HuggingFace, PEFT, LoRA/QLoRA, PyTorch, JSON schemas | 4 Weeks |
| **P6** | [AI Security & Guardrails](file:///Users/biswanathgiri/Desktop/project-based-agentic-ai-learning/P6-ai-security-guardrails/README.md) | Safety & Compliance | google-antigravity (ADK) policy engine, Microsoft Presidio, FastAPI | 4 Weeks |

---

## 🛠️ Course-Wide Prerequisites & Setup

### 1. System Requirements
- **OS:** macOS / Linux / Windows 11 (with WSL2).
- **Python:** Python `3.10` or `3.11` (recommended).
- **Docker:** Docker Desktop installed and running.
- **Minikube:** Required for **Project 3** (Kubernetes deployment).

### 2. Global Environment Setup
Clone this repository and create a virtual environment:
```bash
# Clone the repository
git clone <repository-url>
cd project-based-agentic-ai-learning

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install global tools
pip install --upgrade pip
```

### 3. API Keys Requirements
These projects run on the Google Gemini model ecosystem. You must obtain a **Gemini API Key** from Google AI Studio and place it in the `.env` files of each project:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
If you do not have a key, you can acquire one for free from: [Google AI Studio API Keys](https://aistudio.google.com/app/api-keys).

---

## 📂 Project Navigation

- 🔍 **[Project 1: Enterprise RAG Assistant](file:///Users/biswanathgiri/Desktop/project-based-agentic-ai-learning/P1-enterprise-rag/README.md)**
  Build a RAG Agent equipped with a custom file search tool (ChromaDB hybrid retrieval) using the google-antigravity (ADK) framework.
- 🤖 **[Project 2: Multi-Agent AI System](file:///Users/biswanathgiri/Desktop/project-based-agentic-ai-learning/P2-multi-agent-system/README.md)**
  Configure a multi-agent Cloud Migration Advisor utilizing google-antigravity subagent capabilities and shared ToolContext states.
- 📦 **[Project 3: LLMOps & AI DevOps](file:///Users/biswanathgiri/Desktop/project-based-agentic-ai-learning/P3-llmops-devops/README.md)**
  Serve an Antigravity agent through FastAPI and deploy it to local Kubernetes, tracking token telemetry and reasoning metrics.
- 📊 **[Project 4: AI Evaluation Platform](file:///Users/biswanathgiri/Desktop/project-based-agentic-ai-learning/P4-ai-evaluation/README.md)**
  Evaluate Antigravity agents' output faithfulness, answer relevancy, and tool-calling execution times using DeepEval/RAGAS.
- ⚙️ **[Project 5: Fine-Tuning Pipeline](file:///Users/biswanathgiri/Desktop/project-based-agentic-ai-learning/P5-fine-tuning-pipeline/README.md)**
  Train model weights to output strict JSON matching Pydantic configurations for agent schemas.
- 🛡️ **[Project 6: AI Security & Guardrails](file:///Users/biswanathgiri/Desktop/project-based-agentic-ai-learning/P6-ai-security-guardrails/README.md)**
  Secure agent instances using Antigravity's native safety policy engine (blocking shell commands, workspace checking, argument predicates).

---

## 📝 Assessment & Grading Policies
Each project contains its own targeted 100-point rubric, focusing on:
* **Functionality & Performance (30%)** - Does the agent execute and utilize tools correctly?
* **ADK Architecture & Design (20%)** - Are configurations, capabilities, and hooks appropriately structured?
* **Verification & Testing (20%)** - Did the student run evaluations or benchmarks?
* **Documentation & Readme (15%)** - Detailed walkthroughs and clear execution parameters.
* **Advanced Extensions (15%)** - Completion of advanced extension tasks (e.g. MCP integration).
