# Project 2: Multi-Agent AI System
*Duration: 4 Weeks | Focus: Agentic AI & Orchestration*

## 📖 Project Brief
Students will build a **Cloud Migration Advisor** using a multi-agent orchestration framework powered by the **Google Antigravity SDK (ADK)**. The system instantiates a Lead Coordinator Agent and delegates tasks to three specialized subagents (Infrastructure Specialist, Cost optimization Agent, and Security compliance Agent) using shared context prompts and tool execution.

---

## 🎯 Learning Objectives
- Learn role-based agent design and system instructions in the Antigravity SDK.
- Understand subagent delegation capabilities (`CapabilitiesConfig(enable_subagents=True)`).
- Implement state-sharing paradigms inside agent prompts.
- Understand how to stream agent thoughts (reasoning logs) and final responses in terminal interfaces.
- Design cooperative multi-agent task descriptions.

---

## 🏗️ Project Architecture Diagram

```
+------------------------------------------------------------------------+
|                      ADK MULTI-AGENT ARCHITECTURE                      |
+------------------------------------------------------------------------+
|                                                                        |
|                           [User Query Input]                           |
|                                   │                                    |
|                                   ▼                                    |
|                    +─────────────────────────────+                     |
|                    │  Lead Coordinator Agent     │                     |
|                    │  (Architect Coordinator)     │                     |
|                    +──────────────┬──────────────+                     |
|                                   │                                    |
|             ┌─────────────────────┼─────────────────────┐              |
|             ▼ (Spawns)            ▼ (Spawns)            ▼ (Spawns)     |
|      +──────────────+      +──────────────+      +──────────────+      |
|      │Infrastructure│      │Cost Optimizer│      │ Security     │      |
|      │  Subagent    │      │  Subagent    │      │  Subagent    │      |
|      +──────┬───────+      +──────┬───────+      +──────┬───────+      |
|             │                     │                     │              |
|             └─────────────────────┼─────────────────────┘              |
|                                   │ (Aggregates Specialist Feedback)   |
|                                   ▼                                    |
|                    +─────────────────────────────+                     |
|                    │  Lead Coordinator Agent     │                     |
|                    │  (Synthesizes Final Report) │                     |
|                    +──────────────┬──────────────+                     |
|                                   │                                    |
|                                   ▼                                    |
|                       [Advisor Output Report]                          |
|                                                                        |
+------------------------------------------------------------------------+
```

---

## 🚦 Step-by-Step Implementation Guide

Follow these steps to build and run the Multi-Agent System:

1. **Environment Setup:** Create a virtual environment and install frameworks from `requirements.txt`.
2. **Setup API Credentials:** Configure your Gemini API keys in the `.env` file.
3. **Define Specialist Personas:** Document the backstories, objectives, and parameters for the 3 specialized subagents (Infrastructure, Cost, Security).
4. **Draft Coordinator Instructions:** In `src/agents.py`, construct system instructions for the coordinator explaining the subagent specialist roles and delegation workflow.
5. **Enable Subagent Capabilities:** Initialize a `CapabilitiesConfig(enable_subagents=True)` parameters object in `src/agents.py`.
6. **Compose Agent Config:** Create `get_coordinator_config` in `src/agents.py` returns `LocalAgentConfig` populated with instructions and capability switches.
7. **Setup main loop:** In `src/main.py`, setup an async wrapper to run the agent chat query.
8. **Instantiate Main Agent:** Initialize the coordinator using `async with Agent(config) as agent:` in `src/main.py`.
9. **Orchestrate Task Query:** Call `agent.chat(prompt)` requesting the coordinator to delegate tasks sequentially to the 3 subagents.
10. **Stream Thought Output:** Capture response logs using `async for thought in response.thoughts` to display reasoning traces.
11. **Print Aggregated Report:** Call `await response.text()` to display the final report.
12. **Configure Verification Fallback:** Implement simulated prints displaying local fallback execution steps in `src/main.py` if the LLM environment is missing.

---

## 📅 Week-by-Week Deliverables

### Week 1: Configuration Design & Setup
- Install dependencies, outline subagent parameters.
- **Deliverable:** `src/agents.py` with coordinator layout and custom instructions.

### Week 2: Persona Definitions
- Finalize specialist agent backstories and task delegation rules.
- **Deliverable:** Config logs mapping agent constraints.

### Week 3: Multi-Agent Integration
- Construct the async run agent loop inside the CLI wrapper.
- **Deliverable:** Main agent compiling subagent query loops.

### Week 4: Execution & Testing
- Run test cloud migration query scripts and check response times and token outputs.
- **Deliverable:** Executable `src/main.py` client output report.

---

## 📊 Grading Rubric (100 Points)

| Criteria | Weight | Description |
| :--- | :--- | :--- |
| **System Instruction Clarity** | 20% | Quality and clarity of coordinator instructions steering delegation patterns. |
| **Capabilities Configuration** | 20% | Correct implementation of subagent enabling configs. |
| **Multi-Agent Execution** | 30% | Correct execution of subagent responses and reports output compilation. |
| **CLI & Output Presentation** | 15% | Clean terminal banner outputs showing clear agent thoughts logging. |
| **Code Structure & Readme** | 15% | Clean Python coding styles and detailed guide. |

---

## 🛠️ Troubleshooting & Tips
- **Thought-Streaming Failures:** Ensure you are accessing the `.thoughts` generator correctly inside the async loop. Not all model identifiers support reasoning traces.
- **VRAM limit:** Using subagents can result in nested model execution. If using local offline fallbacks, CPU metrics should remain clean.
