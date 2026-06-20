import os
from google.antigravity import LocalAgentConfig, types

def get_coordinator_config() -> LocalAgentConfig:
    """
    Returns the LocalAgentConfig for the main Coordinator Agent.
    Enables subagent capabilities so the coordinator can spawn specialists.
    """
    # System instructions describing the specialists the coordinator can delegate to.
    system_instructions = (
        "You are the Lead Cloud Migration Architect Coordinator. "
        "Your task is to coordinate a cloud migration review using specialized subagents.\n\n"
        "You have access to 3 specialist profiles that you can spawn as subagents:\n"
        "1. Infrastructure Agent: Expert in network isolation, VM sizes, load balancers, and Kubernetes topologies.\n"
        "2. Cost Optimization Agent: FinOps specialist expert in sizing savings, Spot instances, and pricing plans.\n"
        "3. Security Compliance Agent: Cloud auditor expert in KMS, IAM restrictions, TLS 1.3, and SOC2 compliance.\n\n"
        "Workflow:\n"
        "- First, instruct the Infrastructure Agent to propose a high-availability server layout for the user query.\n"
        "- Second, pass that layout to the Cost Optimization Agent to verify cost savings recommendations.\n"
        "- Third, pass the optimized layout to the Security Compliance Agent to run a policy check.\n"
        "- Finally, aggregate all individual feedbacks into a single structured final advisory report."
    )
    
    return LocalAgentConfig(
        system_instructions=system_instructions,
        capabilities=types.CapabilitiesConfig(
            enable_subagents=True  # Enables the coordinator to delegate tasks
        )
    )
