import os
from dotenv import load_dotenv

load_dotenv()

class BaseAgent:
    """
    Simulates a CrewAI-style Agent for educational simplicity, 
    allowing execution with either Gemini or offline fallbacks.
    """
    def __init__(self, role: str, goal: str, backstory: str):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.api_key = os.getenv("GEMINI_API_KEY")

    def _get_system_prompt(self) -> str:
        return (
            f"You are the {self.role}.\n"
            f"Your Goal: {self.goal}\n"
            f"Your Backstory: {self.backstory}\n"
            f"Provide professional, structured outputs. Do not break character."
        )

    def execute(self, prompt: str) -> str:
        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                model = genai.GenerativeModel(
                    model_name=os.getenv("LLM_MODEL", "gemini-1.5-flash"),
                    system_instruction=self._get_system_prompt()
                )
                response = model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                print(f"[Agent Execution Warning] API Call failed: {e}. Falling back to offline simulation.")
        
        # Fallback offline simulation
        return self._simulate_response(prompt)

    def _simulate_response(self, prompt: str) -> str:
        raise NotImplementedError("Each simulated agent must define fallback responses.")


class InfrastructureAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Cloud Infrastructure Specialist",
            goal="Design a high-availability, scalable server and network architecture.",
            backstory="You have 15 years of experience deploying AWS and Azure architectures. You focus on Kubernetes, VMs, load balancers, and network isolation."
        )

    def _simulate_response(self, prompt: str) -> str:
        return (
            "### INFRASTRUCTURE ARCHITECTURE PLAN\n"
            "- **Compute Nodes:** Deploy 3x EC2 t3.medium VMs in an Auto-Scaling Group across Multi-AZs.\n"
            "- **Database:** Deploy AWS RDS MySQL instance (db.t3.medium) with Multi-AZ replication enabled.\n"
            "- **Network:** Configure 1x public subnet (for Load Balancer) and 2x private subnets for application and database nodes.\n"
            "- **Handoff:** Ready for cost optimization audit."
        )


class CostAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Cloud Cost Optimization Specialist",
            goal="Verify infrastructure plans and optimize them for the lowest possible cost.",
            backstory="You are a certified FinOps practitioner. You analyze VM sizes, reserve instances, and ensure no over-provisioning happens."
        )

    def _simulate_response(self, prompt: str) -> str:
        return (
            "### FINOPS COST REVIEW\n"
            "- **Compute Savings:** Recommend swapping t3.medium to t3.micro for the staging environment (-$30/mo savings).\n"
            "- **Database Savings:** Reconsider Multi-AZ RDS for non-production environments to save 50% ($60/mo -> $30/mo).\n"
            "- **Total Estimate:** Target monthly cloud cost reduced from $180/mo to $95/mo."
        )


class SecurityAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Cloud Security Compliance Officer",
            goal="Evaluate architectures for SOC2, HIPAA, and general data encryption requirements.",
            backstory="You are an expert cloud security auditor. You enforce HTTPS, KMS database encryption, and strict IAM roles."
        )

    def _simulate_response(self, prompt: str) -> str:
        return (
            "### SECURITY & COMPLIANCE REVIEW\n"
            "- **Data at Rest:** Databases must have KMS AES-256 encryption enabled.\n"
            "- **Data in Transit:** Ingress controllers must enforce HTTPS (TLS 1.3) configurations.\n"
            "- **IAM Policy:** Enforce Principle of Least Privilege. Restrict root SSH access completely.\n"
            "- **Audit Result:** PASSED (Assuming policies are applied)."
        )
