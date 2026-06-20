import os
import time
import json
import asyncio
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from presidio_helper import PIIRedactor
from injection_detector import InjectionDetector
from dotenv import load_dotenv

# Import google-antigravity SDK safety policies
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.hooks import policy

load_dotenv()

app = FastAPI(
    title="ADK Agent Security Wrapper Gateway",
    description="Protects Antigravity Agents using Microsoft Presidio and ADK Policy engines",
    version="1.0"
)

# ----------------- SECURITY COMPONENTS -----------------
pii_redactor = PIIRedactor()
injection_detector = InjectionDetector()
AUDIT_LOG_FILE = "./security_audit.log"

def write_audit_log(event_type: str, details: dict):
    log_entry = {
        "timestamp": time.time(),
        "event_type": event_type,
        "details": details
    }
    with open(AUDIT_LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

# ----------------- SCHEMAS -----------------
class SecureChatRequest(BaseModel):
    user_query: str

class SecureChatResponse(BaseModel):
    safe_response: str
    redacted_query_used: str
    sanitized_output: bool
    blocked: bool
    latency_ms: float

# ----------------- ADK SECURED INFERENCE -----------------
async def run_secured_agent(prompt: str) -> str:
    """
    Executes the google-antigravity Agent query wrapped in safety policies.
    """
    # 1. Define policies: Deny run_command completely, restrict workspace
    allowed_workspaces = [os.path.abspath("./")]
    
    agent_policies = [
        policy.deny("run_command"), # Prevent shell executions
        policy.workspace_only(allowed_workspaces), # Restrict file tools to current folder
        # Predicate check: Deny tool call if arguments contain high risk terms
        policy.deny(
            "*", 
            when=lambda args: any("rm -rf" in str(v) for v in args.values()),
            name="deny_rm_rf"
        )
    ]
    
    config = LocalAgentConfig(
        system_instructions="You are a safe internal assistant. Obey all safety guidelines.",
        policies=agent_policies
    )
    
    async with Agent(config=config) as agent:
        response = await agent.chat(prompt)
        return await response.text()

# ----------------- ENDPOINTS -----------------

@app.middleware("http")
async def log_latency_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "unknown"
    start_time = time.time()
    response = await call_next(request)
    latency = (time.time() - start_time) * 1000
    print(f"[Secured Gateway IP] {request.method} {request.url.path} from IP: {client_ip} | Latency: {latency:.2f}ms")
    return response

@app.post("/secure-chat", response_model=SecureChatResponse)
def secure_chat(request: SecureChatRequest):
    start_time = time.time()
    query = request.user_query
    
    # 1. Inspect for Prompt Injection
    if injection_detector.is_injection(query):
        write_audit_log("INJECTION_ATTEMPT", {"query": query[:250], "action": "blocked"})
        raise HTTPException(
            status_code=400, 
            detail="Request blocked: Potential prompt injection attempt detected."
        )

    # 2. Redact PII in prompt (Input Sanitization)
    redacted_query = pii_redactor.redact(query)
    
    # 3. Call Secured Antigravity Agent
    api_key_set = bool(os.getenv("GEMINI_API_KEY"))
    try:
        if api_key_set:
            raw_response = asyncio.run(run_secured_agent(redacted_query))
            mode = "ADK-SECURE-GEMINI"
        else:
            raw_response = f"[Simulated Response] Safe answer to query: '{redacted_query}'."
            mode = "ADK-SECURE-OFFLINE"
    except Exception as e:
        write_audit_log("POLICY_VIOLATION_BLOCKED", {"error": str(e)})
        raise HTTPException(status_code=403, detail=f"Request blocked by ADK Safety Policies: {e}")

    # 4. Inspect Output PII leak
    safe_response = pii_redactor.redact(raw_response)
    output_sanitized = safe_response != raw_response
    
    latency_ms = (time.time() - start_time) * 1000

    return SecureChatResponse(
        safe_response=safe_response,
        redacted_query_used=redacted_query,
        sanitized_output=output_sanitized,
        blocked=False,
        latency_ms=round(latency_ms, 2)
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
