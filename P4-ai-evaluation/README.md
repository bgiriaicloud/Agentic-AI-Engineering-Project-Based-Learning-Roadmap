# Project 4: AI Evaluation Platform
*Duration: 4 Weeks | Focus: Quality Assurance & Testing*

## 📖 Project Brief
Students will build a quality assurance platform to evaluate **Google Antigravity SDK (ADK)** agent responses for accuracy, relevance, context recall, and hallucination prevention using industry-standard libraries: RAGAS and DeepEval. Students will build a dashboard to log and review evaluation runs.

---

## 🎯 Learning Objectives
- Learn standard evaluation parameters for LLMs: Faithfulness, Answer Relevance, Context Recall, Context Precision, and Semantic Drift.
- Understand how to generate a **Golden Dataset** (test case generation using raw contexts).
- Integrate evaluations dynamically with an active `google-antigravity` agent session.
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
|                                            [Antigravity Agent]         |
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
2. **Setup Credentials:** Configure Gemini API keys in the `.env` file.
3. **Inspect Evaluation Dataset:** Examine `data/golden_dataset.json` containing query, context, and candidate outputs.
4. **Implement Synthetic Data Generator:** Write the code inside `src/generate_testset.py` to simulate context-to-QA mappings.
5. **Add New Synthetic Cases:** Run `python src/generate_testset.py` to verify the synthetic case is appended to the golden dataset file.
6. **Build Evaluator Engine:** Define the `RAGEvaluator` class in `src/evaluator.py` to load test cases.
7. **Hook Antigravity Agent:** Write `get_agent_response` inside `src/evaluator.py` utilizing `Agent(LocalAgentConfig())` to fetch live responses for test prompts.
8. **Implement Scorer Prompts:** Create scoring prompts inside `src/evaluator.py` requesting a decimal score from the evaluator model.
9. **Implement Fallback Math Scorers:** Code fallback token overlap algorithms inside `src/evaluator.py` to allow tests to run offline.
10. **Log Metric Outcomes:** Configure the `run_suite` function in `src/evaluator.py` to compute metrics values and write outcomes to `evaluation_results.json`.
11. **Build Streamlit Dashboard:** Design the visualization page in `src/dashboard.py` containing pandas dataframes, average score cards, and comparison layouts.
12. **Verify Telemetry charts:** Execute the suite using the sidebar button on the dashboard interface and review score comparisons between grounded (v1) and hallucinated (v2) runs.

---

## 📅 Week-by-Week Deliverables

### Week 1: Evaluation Framework setup
- Install libraries and configure evaluation schemas.
- Understand synthetic test generation.
- **Deliverable:** `src/generate_testset.py` to compile ground-truth data.

### Week 2: Metric Implementation
- Implement Faithfulness and Answer Relevancy using RAGAS/DeepEval.
- **Deliverable:** `data/golden_dataset.json` loaded and ran through base queries.

### Week 3: Regression Testing Script
- Write a Python execution script that evaluates google-antigravity agent outputs and asserts strict thresholds.
- **Deliverable:** `src/evaluator.py` which runs tests and logs outputs.

### Week 4: Dashboard & Reporting
- Develop a Streamlit application to visualize performance scores, failed test cases, and metric drift over time.
- **Deliverable:** Full `src/dashboard.py` dashboard running.

---

## 📊 Grading Rubric (100 Points)

| Criteria | Weight | Description |
| :--- | :--- | :--- |
| **Test Case Design** | 20% | Quality and validity of QA pairs in `golden_dataset.json`. |
| **Metrics Engine** | 30% | Correct implementation of faithfulness and relevance metrics on active ADK outputs. |
| **Automation & CLI** | 20% | Correct execution of regression scoring CLI that outputs summary report logs. |
| **Streamlit Dashboard** | 20% | Beautiful, user-friendly visualization of metrics scores, showing clear passes and failures. |
| **Extension Tasks** | 10% | Add custom NLP metric scorers (e.g. BLEU, ROUGE, or custom semantic vectors similarity). |
