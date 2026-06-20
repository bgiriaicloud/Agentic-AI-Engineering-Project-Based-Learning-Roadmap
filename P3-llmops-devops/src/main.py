import time
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

app = FastAPI(
    title="AI Sentiment Inference API",
    description="Microservice with Prometheus instrumentation",
    version="1.0"
)

# ----------------- PROMETHEUS INSTRUMENTATION -----------------
# Metrics tracking: request rates, labels (sentiment), and execution time
INFERENCE_REQUESTS = Counter(
    "inference_requests_total",
    "Total number of inference requests processed",
    ["status", "prediction"]
)

INFERENCE_LATENCY = Histogram(
    "inference_latency_seconds",
    "Time taken to run inference in seconds",
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

# ----------------- MODEL LOADER -----------------
# Lazy load Hugging Face pipeline, fall back to mock classification if unavailable offline.
classifier = None

def get_classifier():
    global classifier
    if classifier is None:
        try:
            print("Loading HuggingFace sentiment analysis pipeline...")
            from transformers import pipeline
            # Load small DistilBERT model
            classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
            print("Model loaded successfully.")
        except Exception as e:
            print(f"[Model Warning] Could not load HuggingFace Pipeline: {e}. Falling back to Rule-Based Sim-Model.")
            classifier = "MOCK"
    return classifier

# ----------------- SCHEMAS -----------------
class InferenceRequest(BaseModel):
    text: str

class InferenceResponse(BaseModel):
    text: str
    label: str
    score: float
    latency_seconds: float
    mode: str

# ----------------- ENDPOINTS -----------------

@app.get("/")
def health_check():
    # Simple endpoint for liveness probe
    return {"status": "healthy", "service": "inference-api"}

@app.get("/ready")
def readiness_check():
    # Verify model is ready to serve queries
    model = get_classifier()
    if model is None:
        raise HTTPException(status_code=503, detail="Model is still loading")
    return {"status": "ready"}

@app.post("/predict", response_model=InferenceResponse)
def predict(request: InferenceRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text input cannot be empty")
        
    start_time = time.time()
    
    # Run prediction
    model = get_classifier()
    label = "UNKNOWN"
    score = 0.0
    mode = "LLM-Local"
    
    try:
        if model == "MOCK":
            mode = "OFFLINE-SIM"
            # Simple keyword mock classifier for offline stability
            lower_text = request.text.lower()
            positive_words = ["good", "love", "happy", "excellent", "awesome", "great", "recommend"]
            negative_words = ["bad", "sad", "fail", "slow", "terrible", "waste", "hate", "issue"]
            
            pos_count = sum(1 for w in positive_words if w in lower_text)
            neg_count = sum(1 for w in negative_words if w in lower_text)
            
            if pos_count > neg_count:
                label = "POSITIVE"
                score = 0.85 + (0.02 * pos_count)
            elif neg_count > pos_count:
                label = "NEGATIVE"
                score = 0.85 + (0.02 * neg_count)
            else:
                label = "POSITIVE"
                score = 0.50
        else:
            # Run HuggingFace prediction
            result = model(request.text)[0]
            label = result["label"]
            score = result["score"]
            
        latency = time.time() - start_time
        
        # Record metrics
        INFERENCE_REQUESTS.labels(status="success", prediction=label).inc()
        INFERENCE_LATENCY.observe(latency)
        
        return InferenceResponse(
            text=request.text,
            label=label,
            score=round(score, 4),
            latency_seconds=round(latency, 4),
            mode=mode
        )
        
    except Exception as e:
        INFERENCE_REQUESTS.labels(status="error", prediction="NONE").inc()
        raise HTTPException(status_code=500, detail=f"Inference failure: {e}")

@app.get("/metrics")
def metrics():
    """
    Exposes metrics for Prometheus scraper.
    """
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    import uvicorn
    # Warmup model loading
    get_classifier()
    uvicorn.run(app, host="0.0.0.0", port=8000)
