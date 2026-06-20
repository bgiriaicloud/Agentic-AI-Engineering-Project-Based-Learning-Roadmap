# Project 6: AI Security & Guardrails
*Duration: 4 Weeks | Focus: Safety & Compliance*

## 📖 Project Brief
Students will build a security middleware wrapping LLM endpoints to detect prompt injection attacks, automatically redact Personally Identifiable Information (PII/PHI) using Microsoft Presidio, and enforce safety guardrails on output content to prevent toxic output and leaks.

---

## 🎯 Learning Objectives
- Understand common LLM vulnerabilities (Prompt Injection, Jailbreaking, System Prompt Extraction).
- Integrate **Microsoft Presidio** to analyze and redact telephone numbers, credit cards, emails, names, and IP addresses.
- Write robust, heuristic-based and vector-based **Prompt Injection Detectors**.
- Understand rate limiting and IP access lists for AI APIs.
- Evaluate the latency-security tradeoff when chain-processing multiple security wrapper filters.

---

## 🏗️ Project Architecture Diagram

```
+------------------------------------------------------------------------+
|                 AI API WRAPPER SECURITY GATEWAY FLOW                   |
+------------------------------------------------------------------------+
|                                                                        |
|  [User Query Input] (Prompt + sensitive data)                          |
|         │                                                              |
|         ▼ (IP validation & Rate limiting)                              |
|  [FastAPI HTTP Middleware]                                             |
|         │                                                              |
|         ▼ (Check keywords & semantic embedding similarity)             |
|  [Injection Detector] ──► (Triggered?) ──► [400 Blocked Response]      |
|         │ (Safe)                                                       |
|         ▼ (Apply Microsoft Presidio Redactor)                          |
|  [PII Input Redactor] (John Doe -> <PERSON>, 555-1234 -> <PHONE>)       |
|         │                                                              |
|         ▼ (Send sanitized prompt to backend LLM)                       |
|  [Gemini API / LLM Engine]                                             |
|         │                                                              |
|         ▼ (Examine response text for accidental leaks)                 |
|  [PII Output Redactor]                                                 |
|         │                                                              |
|         ▼ (Record logs to security_audit.log)                          |
|  [Audit Logging Node]                                                  |
|         │                                                              |
|         ▼ (Return safe JSON response)                                  |
|  [Client Response Output]                                              |
|                                                                        |
+------------------------------------------------------------------------+
```

---

## 🚦 Step-by-Step Implementation Guide

Follow these steps to build and execute the AI Security Wrapper:

1. **Environment Setup:** Set up your Python virtual environment and install dependencies listed in `requirements.txt`.
2. **Setup Language Model Assets:** Download the English language package for spaCy (`python -m spacy download en_core_web_sm`) to support Presidio.
3. **Setup Credentials:** Add your Gemini API keys to the `.env` file.
4. **Build PII Redactor:** Write the `PIIRedactor` class in `src/presidio_helper.py` that wraps Microsoft Presidio's Analyzer and Anonymizer engines.
5. **Implement Regex Fallbacks:** Code regex replacements for emails and cards inside `src/presidio_helper.py` in case Presidio fails to initialize offline.
6. **Implement Injection Keywords:** Define high-risk prompt injection keywords (e.g. "ignore all instructions") in `src/injection_detector.py`.
7. **Implement Semantic Injection Checks:** Code similarity comparisons using SentenceTransformers inside `src/injection_detector.py` to compare inputs against known jailbreaks.
8. **Build API Middleware:** Set up the FastAPI framework in `src/guard_wrapper.py` with custom middleware capturing client IP addresses.
9. **Implement Pipeline Logic:** In the `/secure-chat` endpoint, coordinate prompt verification: check injection, redact PII, call LLM, and sanitize outbound response.
10. **Implement Audit Log:** Code the `write_audit_log` function in `src/guard_wrapper.py` to write JSON audit trails to `security_audit.log`.
11. **Run & Test Security:** Launch the server (`python src/guard_wrapper.py`) and test normal vs jailbreak inputs to verify blocks.
12. **Review Latency Logs:** Check the printed output log statements to analyze the execution latency of your security filters.

---

## 📅 Week-by-Week Deliverables

### Week 1: Security Framework Setup
- Build baseline FastAPI server wrappers.
- Learn PII concepts and identify rules.
- **Deliverable:** FastAPI base code and documentation.

### Week 2: Input Sanitization (PII Redaction)
- Integrate Microsoft Presidio Analyzer and Anonymizer engines.
- Write custom PII rule matches (e.g. for custom internal employee ID formats).
- **Deliverable:** `src/presidio_helper.py` showing working redaction.

### Week 3: Prompt Injection Protection
- Implement detection rules (regex check, heuristic patterns, and similarity matching against known jailbreak vectors).
- **Deliverable:** `src/injection_detector.py` showing blocking of malicious inputs.

### Week 4: Output Guardrails & Audits
- Hook input and output checks into a combined FastAPI routing pipeline.
- Implement security audit log generation for tracking security triggers.
- **Deliverable:** Completed `src/guard_wrapper.py` middleware running locally.

---

## 📁 Repository Structure
```
P6-ai-security-guardrails/
├── README.md
├── requirements.txt
├── .env.example
└── src/
    ├── presidio_helper.py
    ├── injection_detector.py
    └── guard_wrapper.py
```

---

## 🚀 Setup & Execution

### 1. Install Dependencies
Ensure your virtual environment is active:
```bash
pip install -r requirements.txt
```
*Note: Microsoft Presidio requires downloading a spaCy language model. Run:*
```bash
python -m spacy download en_core_web_sm
```

### 2. Configure Environment
```bash
cp .env.example .env
```
Ensure your `GEMINI_API_KEY` is present.

### 3. Start the Secured API Wrapper
```bash
python src/guard_wrapper.py
```
Test endpoints using Swagger docs at `http://localhost:8000/docs`.

---

## 📊 Grading Rubric (100 Points)

| Criteria | Weight | Description |
| :--- | :--- | :--- |
| **PII Redaction Engine** | 30% | Correct integration of Presidio; successfully redacts emails, credit cards, and names from inputs. |
| **Prompt Injection Protection** | 30% | Accurately identifies jailbreak attempts (e.g., "ignore prior instructions") and aborts execution. |
| **API Middleware Wrapper** | 20% | Correct coordination of security pipeline phases in FastAPI; provides clear audit logs. |
| **Code Performance** | 10% | Latency is kept minimal during scanning phases. |
| **Documentation & Readme** | 10% | Setup instructions and testing procedures are detailed. |

---

## 🛠️ Troubleshooting & Tips
- **Presidio Language Model Error:** If Presidio complains about missing spaCy models, confirm you ran `python -m spacy download en_core_web_sm` and restarted your server.
- **False Positives:** If your injection detector is too sensitive, it might block legitimate requests. Fine-tune your similarity thresholds or validation rules in `src/injection_detector.py`.
