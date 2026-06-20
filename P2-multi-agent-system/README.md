# Project 2: Multi-Agent AI System
*Duration: 4 Weeks | Focus: Agentic AI & Orchestration*

## 📖 Project Brief
Students will build a **Cloud Migration Advisor** using a multi-agent orchestration framework (LangGraph and CrewAI). The system coordinates three specialized agents (Infrastructure Agent, Cost Optimization Agent, and Security Compliance Agent) to review cloud migration requests and produce an integrated cloud deployment plan.

---

## 🎯 Learning Objectives
- Learn role-based agent design and system prompting techniques.
- Understand the difference between sequential crew workflows and cyclic state-machine graph architectures.
- Implement state variables and message-based memory storage in LangGraph.
- Master agent routing, conditional branching, and collaborative agent tasks.
- Control state transitions dynamically based on structured output models.

---

## 🏗️ Project Architecture Diagram

```
+------------------------------------------------------------------------+
|                 LANGGRAPH MULTI-AGENT STATE GRAPH                      |
+------------------------------------------------------------------------+
|                                                                        |
|                           [User Query Input]                           |
|                                   │                                    |
|                                   ▼                                    |
|                       +────────────────────────+                       |
|                       │  Infrastructure Node   │◄────────────────+     |
|                       │ (InfrastructureAgent)  │                 │     |
|                       +───────────┬────────────+                 │     |
|                                   │                              │     |
|                                   ▼                              │     |
|                       +────────────────────────+                 │     |
|                       │       Cost Node        │                 │ (If |
|                       │      (CostAgent)       │                 │ Sec |
|                       +───────────┬────────────+                 │ Warning|
|                                   │                              │ &   |
|                                   ▼                              │ Rev |
|                       +────────────────────────+                 │ < 2)│
|                       │     Security Node      │                 │     |
|                       │     (SecurityAgent)    │                 │     |
|                       +───────────┬────────────+                 │     |
|                                   │                              │     |
|                                   ▼                              │     |
|                        /// Router Decision \\\ ──────────────────+     |
|                        \\\                     ///                     |
|                                   │                                    |
|                                   │ (Else: Safe or Max Revisions)      |
|                                   ▼                                    |
|                       +────────────────────────+                       |
|                       │    Synthesize Node     │                       |
|                       │  (Generates Report)    │                       |
|                       +───────────┬────────────+                       |
|                                   │                                    |
|                                   ▼                                    |
|                                [ END ]                                 |
|                                                                        |
+------------------------------------------------------------------------+
```

---

## 🚦 Step-by-Step Implementation Guide

Follow these steps to build and run the Multi-Agent AI System:

1. **Environment Setup:** Create a virtual environment and install frameworks from `requirements.txt`.
2. **Setup API Credentials:** Configure your Gemini API keys in the `.env` file.
3. **Define Shared Graph State:** In `src/state.py`, define the `MigrationState` structure using a Python `TypedDict` containing all target tracking metrics.
4. **Implement Custom Base Agent:** In `src/agents.py`, implement the base class wrapper `BaseAgent` that handles model prompt formatting and outputs.
5. **Construct Agent Personas:** In `src/agents.py`, instantiate subclasses for `InfrastructureAgent`, `CostAgent`, and `SecurityAgent` with individual backstory goals.
6. **Implement Offline Mock responses:** Add mock fallback logic inside each subclass so the state machine can execute without active internet connections.
7. **Create Graph Nodes:** In `src/graph.py`, define node functions `run_infrastructure`, `run_cost`, and `run_security` that extract the graph state, call their respective agents, and return updated state dicts.
8. **Build Conditional Edge Routing:** Create `security_routing_decision` in `src/graph.py` to check for security warnings and route the workflow back to infrastructure if revision count is less than 2.
9. **Assemble the Workflow Graph:** Initialize the `StateGraph(MigrationState)` structure in `src/graph.py`, attach all nodes, link standard edges, map conditional routes, and compile the application.
10. **Build CLI Entrypoint:** Create `src/main.py` containing terminal output banners, interactive prompt loops, and state compiler triggers.
11. **Test Execution Loops:** Run `python src/main.py` and test standard inputs to verify cyclic paths are executing correctly.
12. **Extend Agent Logic:** Challenge students to add a human-review validation node using LangGraph's native interrupt features.

---

## 📅 Week-by-Week Deliverables

### Week 1: Graph State and Schema Definition
- Install frameworks, design the agent topology.
- Code the shared graph state using Python TypedDict.
- **Deliverable:** `src/state.py` containing structure and schema definitions.

### Week 2: Specialist Agent Definitions
- Define agent roles, backstories, and goals using CrewAI or LangChain.
- Bind local mock tools (e.g. calculator, pricing search, compliance lookup) to agents.
- **Deliverable:** `src/agents.py` with fully populated system instructions and tool bindings.

### Week 3: LangGraph Compilation & Routing
- Define nodes for each specialized agent and write graph transition loops.
- Code the conditional router node to verify if agent suggestions require security revisions or cost refinements.
- **Deliverable:** `src/graph.py` state-machine configuration.

### Week 4: Orchestration & Dashboard execution
- Connect the LangGraph compiler to a console/dashboard interface.
- Implement agent memory to recall state across multiple user messages.
- Run test scenarios and evaluate handoff response times.
- **Deliverable:** Executable `src/main.py` entrypoint.

---

## 📁 Repository Structure
```
P2-multi-agent-system/
├── README.md
├── requirements.txt
├── .env.example
└── src/
    ├── state.py
    ├── agents.py
    ├── graph.py
    └── main.py
```

---

## 🚀 Setup & Execution

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your Gemini API keys:
```bash
cp .env.example .env
```

### 3. Run the Multi-Agent Advisor
Launch the interactive CLI script:
```bash
python src/main.py
```

---

## 📊 Grading Rubric (100 Points)

| Criteria | Weight | Description |
| :--- | :--- | :--- |
| **Graph State Design** | 20% | Proper state schema handling; prevents data loss during agent handoffs. |
| **Agent Roles & Execution** | 30% | Correct system prompting, persona adherence, and modular tool actions. |
| **Routing & Collaboration** | 30% | Correct execution of cyclic graph routing, state checks, and loop prevention. |
| **User Interface & Integration** | 10% | Clean main script execution that outputs a readable final migration report. |
| **Extension Activities** | 10% | Implement human-in-the-loop validation checkpoints in the graph workflow. |

---

## 🛠️ Troubleshooting & Tips
- **Infinite Loops:** If agents route back and forth continuously, check your conditional router logic to ensure loop exit conditions (e.g., maximum loops counter) are strictly enforced.
- **Memory Storage:** To test persistence, run consecutive queries in the CLI interface and verify the agent remembers context from the prior turns.
