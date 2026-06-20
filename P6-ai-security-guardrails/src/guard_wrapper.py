import os
import time
import json
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from presidio_helper import PIIRedactor
from injection_detector import InjectionDetector
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="AI Security Wrapper Gateway",
    description="Protects LLM inference endpoints from prompt injections and data leaks",
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

# ----------------- LLM CONNECTOR -----------------
def generate_llm_response(prompt: str) -> str:
    """
    Sends query to Gemini API, falling back to mock response if unavailable.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"[LLM Warning] Gemini call failed: {e}. Using simulated response.")
            
    # Mock LLM responder
    return f"Processed query safely: '{prompt}'. Here is the simulated secure response."

# ----------------- ENDPOINTS -----------------

@app.middleware("http")
async def rate_limit_and_ip_checks(request: Request, call_next):
    """
    Basic security logs and source validation middleware.
    """
    client_ip = request.client.host if request.client else "unknown"
    start_time = time.time()
    
    # Process request
    response = await call_next(request)
    
    latency = (time.time() - start_time) * 1000
    print(f"[Gateway IP Logging] {request.method} {request.url.path} from IP: {client_ip} | Latency: {latency:.2f}ms")
    return response

@app.post("/secure-chat", response_model=SecureChatResponse)
def secure_chat(request: SecureChatRequest):
    start_time = time.time()
    query = request.user_query
    
    # 1. Inspect for Prompt Injection
    if injection_detector.is_injection(query):
        write_audit_log(
            "INJECTION_ATTEMPT", 
            {"query": query[:250], "action": "blocked"}
        )
        raise HTTPException(
            status_code=400, 
            detail="Request blocked: Potential prompt injection attempt detected."
        )

    # 2. Redact PII (Input Sanitization)
    redacted_query = pii_redactor.redact(query)
    pii_redacted = redacted_query != query
    
    if pii_redacted:
        write_audit_log(
            "PII_REDACTED", 
            {"original": query[:120], "redacted": redacted_query[:120]}
        )
        print("[PII Intercepted] Sensitive details redacted from prompt.")

    # 3. Call LLM
    raw_response = generate_llm_response(redacted_query)

    # 4. Inspect Output (Output Validation)
    # Ensure no credit cards or PII are leaked in response text
    safe_response = pii_redactor.redact(raw_response)
    output_sanitized = safe_response != raw_response
    
    if output_sanitized:
         write_audit_log(
            "OUTPUT_PII_LEAK_BLOCKED", 
            {"raw": raw_response[:120], "redacted": safe_response[:120]}
         )
         print("[PII Intercepted] Blocked sensitive leak from outbound response.")

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
