# 🎯 Agentic AI Engineering Project-Based Learning Roadmap
*Created by Biswanath Giri*

Welcome to the **AI Engineering Project-Based Learning (PBL) Roadmap**. This curriculum is designed to guide college students (3rd/4th year undergraduate or graduate level) through the implementation of real-world, industry-standard AI systems. 

Rather than working on simple minimum viable products, students will build components of an **Enterprise-Grade Agentic AI Platform**.

---

## 📋 Course Curriculum Overview

| Project | Project Name | Primary Focus | Key Technologies | Duration |
| :--- | :--- | :--- | :--- | :--- |
| **P1** | [Enterprise RAG Assistant](file:///Users/biswanathgiri/Desktop/project-based-agentic-ai-learning/P1-enterprise-rag/README.md) | Retrieval-Augmented Generation | Streamlit, ChromaDB, HuggingFace, Gemini API | 4 Weeks |
| **P2** | [Multi-Agent AI System](file:///Users/biswanathgiri/Desktop/project-based-agentic-ai-learning/P2-multi-agent-system/README.md) | Agentic AI & Orchestration | LangGraph, CrewAI, Python state machines | 4 Weeks |
| **P3** | [LLMOps & AI DevOps](file:///Users/biswanathgiri/Desktop/project-based-agentic-ai-learning/P3-llmops-devops/README.md) | MLOps & Deployment | FastAPI, Docker, Kubernetes, Prometheus, Grafana | 4 Weeks |
| **P4** | [AI Evaluation Platform](file:///Users/biswanathgiri/Desktop/project-based-agentic-ai-learning/P4-ai-evaluation/README.md) | Quality Assurance & Testing | RAGAS, DeepEval, Streamlit, QA generation | 4 Weeks |
| **P5** | [Fine-Tuning Pipeline](file:///Users/biswanathgiri/Desktop/project-based-agentic-ai-learning/P5-fine-tuning-pipeline/README.md) | Model Optimization | HuggingFace, PEFT, LoRA/QLoRA, PyTorch | 4 Weeks |
| **P6** | [AI Security & Guardrails](file:///Users/biswanathgiri/Desktop/project-based-agentic-ai-learning/P6-ai-security-guardrails/README.md) | Safety & Compliance | Microsoft Presidio, Guardrails, FastAPI | 4 Weeks |

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
Many of these projects use large language models. The codebases support using the **Google Gemini API** (via `google-genai` or standard SDKs) as well as local fallback models (like Ollama or mock responses if API keys are missing).
To use Gemini, grab a key from Google AI Studio and place it in the respective `.env` files of each project:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 📂 Project Navigation

- 🔍 **[Project 1: Enterprise RAG Assistant](file:///Users/biswanathgiri/Desktop/project-based-agentic-ai-learning/P1-enterprise-rag/README.md)**
  Build a Q&A engine that reads enterprise files, creates semantic vector databases, runs hybrid search, and presents citations.
- 🤖 **[Project 2: Multi-Agent AI System](file:///Users/biswanathgiri/Desktop/project-based-agentic-ai-learning/P2-multi-agent-system/README.md)**
  Build a Cloud Migration Advisor using three specialized agents coordinating with LangGraph.
- 📦 **[Project 3: LLMOps & AI DevOps](file:///Users/biswanathgiri/Desktop/project-based-agentic-ai-learning/P3-llmops-devops/README.md)**
  Containerize a model inference API and deploy it to a local Kubernetes cluster with live Prometheus metrics.
- 📊 **[Project 4: AI Evaluation Platform](file:///Users/biswanathgiri/Desktop/project-based-agentic-ai-learning/P4-ai-evaluation/README.md)**
  Automate hallucination detection and prompt regression tests using RAGAS and DeepEval metrics.
- ⚙️ **[Project 5: Fine-Tuning Pipeline](file:///Users/biswanathgiri/Desktop/project-based-agentic-ai-learning/P5-fine-tuning-pipeline/README.md)**
  Implement a fine-tuning script to train a lightweight LLM on instruction datasets using QLoRA.
- 🛡️ **[Project 6: AI Security & Guardrails](file:///Users/biswanathgiri/Desktop/project-based-agentic-ai-learning/P6-ai-security-guardrails/README.md)**
  Redact PII/PHI datasets automatically and catch prompt injection attacks dynamically.

---

## 📝 Grading Policies & Rubric
Each project contains its own targeted 100-point rubric, focusing on:
* **Functionality & Performance (30%)** - Does the code execute correctly and fulfill the requirements?
* **Code Architecture & Design (20%)** - Are files clean, structured, modular, and well-commented?
* **Verification & Testing (20%)** - Did the student write tests or evaluate results?
* **Documentation & Readme (15%)** - Are installation and run instructions detailed?
* **Advanced Extensions (15%)** - Did the student complete the proposed extension tasks?
