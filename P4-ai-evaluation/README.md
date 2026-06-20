# Project 4: AI Evaluation Platform
*Duration: 4 Weeks | Focus: Quality Assurance & Testing*

## 📖 Project Brief
Students will build a quality assurance platform to evaluate RAG systems and LLM responses for accuracy, relevance, context recall, and hallucination prevention using industry-standard libraries: RAGAS and DeepEval. Students will build a dashboard to log and review evaluation runs.

---

## 🎯 Learning Objectives
- Learn standard evaluation parameters for LLMs: Faithfulness, Answer Relevance, Context Recall, Context Precision, and Semantic Drift.
- Understand how to generate a **Golden Dataset** (test case generation using raw contexts).
- Configure DeepEval metrics to test LLM APIs.
- Set up automated regressions tests that fail a deployment if evaluation metrics fall below a threshold.
- Display score trends and comparison matrices in a Streamlit dashboard.

---

## 🏗️ Project Architecture Diagram

```
+------------------------------------------------------------------------+
|                      RAG EVALUATION PIPELINE ARTIFACTS                 |
+------------------------------------------------------------------------+
|                                                                        |
|  [Raw Context Docs] ──► [Test Generator] ──► [Golden Dataset (JSON)]  |
|                                                     │                  |
|                                                     ▼ (Iterate cases)  |
|                                            [User Question Input]       |
|                                                     │                  |
|                                                     ▼                  |
|                                             [(Target RAG App)]         |
|                                                     │                  |
|                                                     ▼ (Generate response)|
|                                            [Model Response Output]     |
|                                                     │                  |
|                                                     ▼                  |
|                       /// RAGAS & DEEPEVAL METRIC JUDGES \\\           |
|                                                     │                  |
|         +───────────────────────────────────────────┼────────────────+ |
|         ▼ (Is response grounded?)                   ▼ (Is it relevant?) |
|  [ Faithfulness Metric ]                     [ Answer Relevance ]      |
|         │                                           │                  |
|         +─────────────────────► ◄───────────────────+                  |
|                                 │                                      |
|                                 ▼ (Generate scores dataframe)          |
|                       [evaluation_results.json]                        |
|                                 │                                      |
|                                 ▼ (Render UI tables and bar charts)    |
|                      [Streamlit Dashboard Web UI]                      |
|                                                                        |
+------------------------------------------------------------------------+
```

---

## 🚦 Step-by-Step Implementation Guide

Follow these steps to construct the AI Evaluation Platform:

1. **Environment Setup:** Set up your virtual python environment and install all packages in `requirements.txt`.
2. **Setup Credentials:** Configure Gemini API keys in the `.env` file to serve as your LLM evaluator.
3. **Inspect Evaluation Dataset:** Examine `data/golden_dataset.json` containing query, context, ground_truth, and candidate outputs.
4. **Implement Synthetic Data Generator:** Write the code inside `src/generate_testset.py` to simulate how raw context blocks are automatically mapped to QA tuples.
5. **Add New Synthetic Cases:** Run `python src/generate_testset.py` to confirm the synthetic test case is appended to the golden dataset file.
6. **Build Evaluator Engine:** Define the `RAGEvaluator` class in `src/evaluator.py` to load test cases and run checks.
7. **Implement Evaluator LLM Prompts:** Create scoring prompts inside `src/evaluator.py` requesting a decimal score from the evaluator model.
8. **Implement Fallback Math Scorers:** Code the fallback token matching overlap algorithm inside `src/evaluator.py` to allow tests to run offline.
9. **Log Metric Outcomes:** Configure the `run_suite` function in `src/evaluator.py` to compute faithfulness and relevancy values and write outcomes to `evaluation_results.json`.
10. **Build Streamlit Dashboard:** Design the visualization page in `src/dashboard.py` containing pandas dataframes, average score cards, and comparison layouts.
11. **Draft Visual Comparison Charts:** Create bar charts and highlighted cells in the Streamlit app comparing normal grounded outputs (v1) with hallucinated outputs (v2).
12. **Test Automated Regressions:** Execute the suite using the sidebar button on the dashboard interface and review score drift statistics.

---

## 📅 Week-by-Week Deliverables

### Week 1: Evaluation Framework setup
- Install libraries and configure evaluation schemas.
- Understand synthetic test generation.
- **Deliverable:** `src/generate_testset.py` to compile ground-truth data.

### Week 2: Metric Implementation
- Implement Faithfulness (detecting hallucinations) and Answer Relevancy using RAGAS/DeepEval.
- **Deliverable:** `data/golden_dataset.json` loaded and ran through base queries.

### Week 3: Regression Testing Script
- Write a Python execution script that evaluates system outputs and asserts strict thresholds.
- **Deliverable:** `src/evaluator.py` which runs tests and logs outputs.

### Week 4: Dashboard & Reporting
- Develop a Streamlit application to visualize performance scores, failed test cases, and metric drift over time.
- **Deliverable:** Full `src/dashboard.py` dashboard running.

---

## 📁 Repository Structure
```
P4-ai-evaluation/
├── README.md
├── requirements.txt
├── .env.example
├── data/
│   └── golden_dataset.json
└── src/
    ├── generate_testset.py
    ├── evaluator.py
    └── dashboard.py
```

---

## 🚀 Setup & Execution

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Rename `.env.example` to `.env` and enter details:
```bash
cp .env.example .env
```
Ensure `GEMINI_API_KEY` is present.

### 3. Generate Golden Test Set
Create or inspect the test suite:
```bash
python src/generate_testset.py
```

### 4. Execute Evaluation Suite
Run the metrics engine:
```bash
python src/evaluator.py
```

### 5. Launch dashboard
```bash
streamlit run src/dashboard.py
```

---

## 📊 Grading Rubric (100 Points)

| Criteria | Weight | Description |
| :--- | :--- | :--- |
| **Test Case Design** | 20% | Quality and validity of QA pairs in `golden_dataset.json`. |
| **Metrics Engine** | 30% | Correct implementation of faithfulness, hallucination check, and relevance metrics. |
| **Automation & CLI** | 20% | Correct execution of regression scoring CLI that outputs summary report logs. |
| **Streamlit Dashboard** | 20% | Beautiful, user-friendly visualization of metrics scores, showing clear passes and failures. |
| **Extension Tasks** | 10% | Add custom NLP metric scorers (e.g. BLEU, ROUGE, or custom semantic vectors similarity). |

---

## 🛠️ Troubleshooting & Tips
- **DeepEval/RAGAS API failures:** Both libraries make calls to an LLM evaluator (by default OpenAI, but can be configured to Gemini API or simple local token match). The starter code provides a custom local evaluation scoring engine if API keys are missing to ensure code robustness.
- **Out of Memory:** Running local embeddings for evaluator similarity calculations can be memory-heavy. If needed, restart the dev environment.
