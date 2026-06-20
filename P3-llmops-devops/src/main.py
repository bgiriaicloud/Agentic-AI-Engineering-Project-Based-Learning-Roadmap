import time
import os
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from dotenv import load_dotenv
from google.antigravity import Agent, LocalAgentConfig

load_dotenv()

app = FastAPI(
    title="ADK Agent Serving API",
    description="Microservice serving google-antigravity Agent with Prometheus instrumentation",
    version="1.0"
)

# ----------------- PROMETHEUS TELEMETRY METRICS -----------------
AGENT_REQUESTS = Counter(
    "agent_requests_total",
    "Total number of agent requests processed",
    ["status"]
)

AGENT_LATENCY = Histogram(
    "agent_latency_seconds",
    "Time taken to run agent chat turn in seconds",
    buckets=[0.1, 0.5, 1.0, 2.5, 5.0, 10.0]
)

# ----------------- SCHEMAS -----------------
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    query: str
    response: str
    latency_seconds: float
    mode: str

# ----------------- ENDPOINTS -----------------

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "antigravity-agent-api"}

@app.get("/ready")
def readiness_check():
    # Verify API key or fallback setup is available
    return {"status": "ready"}

async def execute_agent_chat(message: str) -> str:
    config = LocalAgentConfig(
        system_instructions="You are a helpful customer support agent. Answer concisely."
    )
    async with Agent(config=config) as agent:
        response = await agent.chat(message)
        return await response.text()

@app.post("/predict", response_model=ChatResponse)
async def predict(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    start_time = time.time()
    api_key_set = bool(os.getenv("GEMINI_API_KEY"))
    
    try:
        if api_key_set:
            # Execute agent chat asynchronously
            agent_output = await execute_agent_chat(request.message)
            mode = "ADK-GEMINI"
        else:
            # Fallback mock offline response
            agent_output = f"[Simulated Response] Received message: '{request.message}' successfully in offline mode."
            mode = "ADK-OFFLINE"
            
        latency = time.time() - start_time
        
        # Record metrics
        AGENT_REQUESTS.labels(status="success").inc()
        AGENT_LATENCY.observe(latency)
        
        return ChatResponse(
            query=request.message,
            response=agent_output,
            latency_seconds=round(latency, 4),
            mode=mode
        )
        
    except Exception as e:
        AGENT_REQUESTS.labels(status="error").inc()
        raise HTTPException(status_code=500, detail=f"Agent execution failure: {e}")

@app.get("/metrics")
def metrics():
    """
    Exposes metrics for Prometheus scraper.
    """
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
