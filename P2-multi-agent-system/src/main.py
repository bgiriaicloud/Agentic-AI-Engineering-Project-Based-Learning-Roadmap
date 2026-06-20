import os
import asyncio
from dotenv import load_dotenv
from agents import get_coordinator_config
from google.antigravity import Agent

load_dotenv()

def print_banner():
    print("""
========================================================================
🤖 CLOUD MIGRATION ADVISOR - ADK MULTI-AGENT ORCHESTRATOR
========================================================================
Powered by google-antigravity SDK (Agent Development Kit)
Specialists online:
  - 🖥️ Infrastructure Subagent
  - 💰 Cost Optimization Subagent
  - 🛡️ Security Compliance Subagent
------------------------------------------------------------------------
""")

async def run_migration_adviser(user_query: str):
    config = get_coordinator_config()
    
    print("\n[ADK Orchestrator] Initializing Lead Advisor Agent...")
    async with Agent(config=config) as agent:
        print("[ADK Orchestrator] Submitting request to Agent hierarchy. Streaming thoughts...")
        print("-" * 50)
        
        # Trigger query execution
        response = await agent.chat(
            f"Analyze this cloud migration request using your specialized subagents: {user_query}"
        )
        
        # Stream model thoughts (reasoning process) if supported
        try:
            async for thought in response.thoughts:
                print(thought, end="", flush=True)
        except Exception:
            # Fallback if thoughts are not supported / not streaming
            pass
            
        print("\n\n" + "=" * 50)
        print("                  FINAL CLOUD ADVISORY REPORT                   ")
        print("=" * 50)
        print(await response.text())
        print("=" * 50)

def main():
    print_banner()
    
    # Pre-defined test inputs or custom query input
    print("Example Queries:")
    print("1. Migrate our database and core application to GCP securely and cost-effectively.")
    print("2. Move our healthcare operations storage to AWS securely.")
    print("3. Deploy a lightweight API for under $30 a month.\n")
    
    query = input("Enter your custom cloud migration query (or press Enter to run Example 1):\n").strip()
    if not query:
        query = "Migrate our database and core application to GCP securely and cost-effectively."
        
    api_key_set = bool(os.getenv("GEMINI_API_KEY"))
    
    if api_key_set:
        try:
            asyncio.run(run_migration_adviser(query))
        except Exception as e:
            print(f"\nExecution encountered an error: {e}. Falling back to offline simulation.")
            api_key_set = False
            
    if not api_key_set:
        # Dry-run offline simulation of subagent delegation
        print("\n[Offline Simulation Mode] Initiating subagent orchestration logs...")
        print("\n  - [Spawning Subagent 1] Infrastructure Specialist:")
        print("    > Layout: RDS replica on GCP Cloud SQL, VMs inside isolated subnet VPC.")
        print("\n  - [Spawning Subagent 2] Cost Optimization Agent:")
        print("    > Optimization: Swap e2-medium VMs to spot instances for staging to save 60%.")
        print("\n  - [Spawning Subagent 3] Security Compliance Officer:")
        print("    > Safety: Force TLS 1.3, restrict database port access via firewalls.")
        print("\n  - [Lead Advisor Aggregating Output] Finalizing Report...")
        print("\n=======================================================")
        print("         SIMULATED CLOUD ADVISORY ADK REPORT           ")
        print("=======================================================")
        print(f"Request: '{query}'")
        print("- Compute: 2x e2-medium (Spot instances config for staging).")
        print("- Storage: GCP Cloud SQL with KMS encryption.")
        print("- Security: VPC networking with strict IAM credentials.")
        print("- Total Est Cost: $65/month (60% saved).")
        print("=======================================================")
        print("\n*Note: Configure a `GEMINI_API_KEY` to run actual async subagent delegation.*")

if __name__ == "__main__":
    main()
