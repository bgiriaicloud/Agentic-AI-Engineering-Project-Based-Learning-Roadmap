import os
from dotenv import load_dotenv
from graph import app_graph
from state import MigrationState

load_dotenv()

def print_banner():
    print("""
========================================================================
🤖 CLOUD MIGRATION ADVISOR - MULTI-AGENT STATE MACHINE
========================================================================
Specialists online:
  - 🖥️ Infrastructure Agent
  - 💰 Cost Optimization Agent
  - 🛡️ Security Compliance Agent
------------------------------------------------------------------------
""")

def main():
    print_banner()
    
    # Pre-defined test inputs or custom query input
    print("Example Queries:")
    print("1. Migrate our company core CRM application to AWS securely and cost-effectively.")
    print("2. Move our healthcare database storage to Google Cloud while maintaining HIPAA standards.")
    print("3. Deploy a lightweight stateless Python API on Azure for < $20 a month.\n")
    
    query = input("Enter your custom cloud migration query (or press Enter to run Example 1):\n").strip()
    if not query:
        query = "Migrate our company core CRM application to AWS securely and cost-effectively."
        
    print(f"\nProcessing query: '{query}'")
    
    # Initialize the workflow state dictionary
    initial_state: MigrationState = {
        "user_query": query,
        "infrastructure_plan": None,
        "cost_review": None,
        "security_compliance_review": None,
        "current_step": "init",
        "revisions_count": 0,
        "final_report": None
    }
    
    # Run the compiled graph state machine
    try:
        final_state = app_graph.invoke(initial_state)
        print("\n--- GRAPH EXECUTION COMPLETED ---\n")
        
        if final_state.get("final_report"):
            print(final_state["final_report"])
        else:
            print("Error: Graph execution completed but no final report was synthesized.")
            
    except Exception as e:
        print(f"\nAn error occurred during state machine execution: {e}")
        print("💡 Hint: Ensure you have installed packages in requirements.txt correctly.")

if __name__ == "__main__":
    main()
