# Project 6: AI Security & Guardrails
*Duration: 4 Weeks | Focus: Safety & Compliance*

## 📖 Project Brief
Students will build a security middleware wrapping LLM endpoints to detect prompt injection attacks, redact Personally Identifiable Information (PII/PHI) using Microsoft Presidio, and enforce safety guardrails using the **Google Antigravity SDK (ADK) Policy Engine** (blocking shell commands, workspace boundaries, and predicate argument checks).

---

## 🎯 Learning Objectives
- Understand common LLM vulnerabilities (Prompt Injection, Jailbreaking, System Prompt Extraction).
- Integrate **Microsoft Presidio** to analyze and redact telephone numbers, credit cards, emails, and names from prompt inputs.
- Configure **Google Antigravity Safety Policies** (`google.antigravity.hooks.policy`) to govern agent tool execution boundaries.
- Set up workspace boundaries using `policy.workspace_only` and enforce argument checks using predicates.
- Log telemetry metrics and compile safety audit logs to track security triggers.

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
|  [PII Input Redactor] (John Doe -> <PERSON>)                           |
|         │                                                              |
|         ▼ (Trigger google-antigravity runtime safety policies)         |
|  [Antigravity Agent Config]                                            |
|    - policy.deny("run_command")                                        |
|    - policy.workspace_only(["./"])                                     |
|    - policy.deny("*", when=lambda args: "rm -rf" in args)              |
|         │                                                              |
|         ▼ (Safety Checked execution via Gemini)                        |
|  [Gemini Model Engine]                                                 |
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
9. **Configure ADK Safety Policies:** In `src/guard_wrapper.py`, establish safety configs utilizing `google.antigravity.hooks.policy`. Deny shell executions (`policy.deny("run_command")`) and set folder parameters.
10. **Implement Custom Safety Predicates:** Write argument checker lambda conditions to deny any tool argument containing high-risk strings (like `rm -rf`).
11. **Assemble Wrapper Logic:** Hook inputs to PII redact, trigger the safe Agent chat run, perform output checks, and write results to `security_audit.log`.
12. **Run & Test Security:** Launch the server (`python src/guard_wrapper.py`) and test normal vs jailbreak inputs to verify policy blocks.

---

## 📅 Week-by-Week Deliverables

### Week 1: Security Framework Setup
- Build baseline FastAPI server wrappers.
- Learn PII concepts and identify rules.
- **Deliverable:** FastAPI base code and documentation.

### Week 2: Input Sanitization (PII Redaction)
- Integrate Microsoft Presidio Analyzer and Anonymizer engines.
- **Deliverable:** `src/presidio_helper.py` showing working redaction.

### Week 3: Prompt Injection Protection
- Implement detection rules (regex check, heuristic patterns, and similarity matching against known jailbreak vectors).
- **Deliverable:** `src/injection_detector.py` showing blocking of malicious inputs.

### Week 4: ADK Safety Policies & Middleware
- Hook safety policies (`policy.deny`, `policy.workspace_only`, arguments predicates) into the active Agent config.
- Run FastAPI endpoint integrations and audit security logs.
- **Deliverable:** Completed `src/guard_wrapper.py` middleware running locally.

---

## 📊 Grading Rubric (100 Points)

| Criteria | Weight | Description |
| :--- | :--- | :--- |
| **PII Redaction Engine** | 20% | Correct integration of Presidio; successfully redacts emails, credit cards, and names from inputs. |
| **Prompt Injection Protection** | 25% | Accurately identifies jailbreak attempts (e.g., "ignore prior instructions") and aborts execution. |
| **ADK Safety Policies Config** | 35% | Correct registration of security policies (blocking commands, workspace boundaries, and predicates checks). |
| **API Middleware Wrapper** | 10% | Correct coordination of security pipeline phases in FastAPI; provides clear audit logs. |
| **Documentation & Readme** | 10% | Setup instructions and testing procedures are detailed. |
