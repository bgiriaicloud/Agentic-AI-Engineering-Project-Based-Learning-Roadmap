from langgraph.graph import StateGraph, END
from state import MigrationState
from agents import InfrastructureAgent, CostAgent, SecurityAgent

# Instantiate the specialized agents
infra_agent = InfrastructureAgent()
cost_agent = CostAgent()
security_agent = SecurityAgent()

# ----------------- NODES -----------------

def run_infrastructure(state: MigrationState) -> MigrationState:
    """
    Formulates a base architecture diagram and specification.
    """
    print("\n[Node] Running Infrastructure Specialist Agent...")
    query = state["user_query"]
    
    # Prompt for infra
    prompt = f"Design an infrastructure plan for this request: {query}"
    infra_plan = infra_agent.execute(prompt)
    
    # Update State
    state["infrastructure_plan"] = infra_plan
    state["current_step"] = "infrastructure"
    return state

def run_cost(state: MigrationState) -> MigrationState:
    """
    Reviews infrastructure proposal and suggests cost optimization actions.
    """
    print("\n[Node] Running Cost Optimization Specialist Agent...")
    infra_plan = state["infrastructure_plan"]
    
    prompt = f"Review this infrastructure layout and provide cost optimizations:\n{infra_plan}"
    cost_review = cost_agent.execute(prompt)
    
    # Update State
    state["cost_review"] = cost_review
    state["current_step"] = "cost"
    return state

def run_security(state: MigrationState) -> MigrationState:
    """
    Reviews infrastructure and cost suggestions for compliance and security issues.
    """
    print("\n[Node] Running Security Compliance Specialist Agent...")
    infra_plan = state["infrastructure_plan"]
    cost_review = state["cost_review"]
    
    prompt = (
        f"Review this infrastructure plan and cost optimizations for SOC2 and safety guidelines:\n"
        f"Infrastructure: {infra_plan}\n"
        f"FinOps Suggestions: {cost_review}"
    )
    security_review = security_agent.execute(prompt)
    
    # Update State
    state["security_compliance_review"] = security_review
    state["current_step"] = "security"
    return state

def run_synthesize(state: MigrationState) -> MigrationState:
    """
    Compiles all reports into a unified migration advisor response.
    """
    print("\n[Node] Running Compilation and Synthesis...")
    
    report = (
        "========================================================================\n"
        "                  CLOUD MIGRATION ADVISOR FINAL REPORT                  \n"
        "========================================================================\n\n"
        f"USER REQUEST: {state['user_query']}\n\n"
        "------------------------------------------------------------------------\n"
        "1. INFRASTRUCTURE PLAN\n"
        "------------------------------------------------------------------------\n"
        f"{state['infrastructure_plan']}\n\n"
        "------------------------------------------------------------------------\n"
        "2. COST OPTIMIZATION (FINOPS) FEEDBACK\n"
        "------------------------------------------------------------------------\n"
        f"{state['cost_review']}\n\n"
        "------------------------------------------------------------------------\n"
        "3. SECURITY & COMPLIANCE FEEDBACK\n"
        "------------------------------------------------------------------------\n"
        f"{state['security_compliance_review']}\n\n"
        "========================================================================"
    )
    
    state["final_report"] = report
    state["current_step"] = "synthesize"
    return state

# ----------------- CONDITIONAL ROUTING -----------------

def security_routing_decision(state: MigrationState):
    """
    Determines if the system needs revision loops due to compliance warnings.
    If security detects severe warnings and revisions < 2, loop back to infra.
    Otherwise, move to final synthesis.
    """
    compliance_text = state["security_compliance_review"] or ""
    revisions = state.get("revisions_count", 0)
    
    # Simple check for warnings
    if "WARNING" in compliance_text.upper() and revisions < 2:
        print(f"\n[Router] ⚠️ Security warnings found. Initiating revision loop {revisions + 1}/2.")
        state["revisions_count"] = revisions + 1
        return "reconstruct_infra"
    
    print("\n[Router] ✅ Plan passes security threshold or max revisions hit. Proceeding to compilation.")
    return "finalize"

# ----------------- BUILD GRAPH -----------------

workflow = StateGraph(MigrationState)

# Add Nodes
workflow.add_node("infrastructure", run_infrastructure)
workflow.add_node("cost", run_cost)
workflow.add_node("security", run_security)
workflow.add_node("synthesize", run_synthesize)

# Define Core Sequential Flow
workflow.set_entry_point("infrastructure")
workflow.add_edge("infrastructure", "cost")
workflow.add_edge("cost", "security")

# Add Conditional Routing from Security
workflow.add_conditional_edges(
    "security",
    security_routing_decision,
    {
        "reconstruct_infra": "infrastructure",
        "finalize": "synthesize"
    }
)

workflow.add_edge("synthesize", END)

# Compile State Machine
app_graph = workflow.compile()
