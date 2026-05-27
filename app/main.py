from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import joblib
from feature_store.features import get_user_features
from feedback.logger import log_prediction, log_click, get_ctr, init_db
from prometheus_client import Counter, Histogram, generate_latest
import pandas as pd

app = FastAPI()

# Load models
model_champion = joblib.load("models/champion/model.pkl")
model_challenger = joblib.load("models/challenger/model.pkl")

# Prometheus metrics
PREDICTION_COUNT = Counter('predictions_total', 'Total predictions', ['model_version'])
CLICK_COUNT = Counter('clicks_total', 'Total clicks', ['model_version'])
LATENCY = Histogram('prediction_latency_seconds', 'Prediction latency')

# Weight for A/B split (80% champion, 20% challenger)
CHAMPION_WEIGHT = 0.8

class RecommendRequest(BaseModel):
    user_id: int

class ClickRequest(BaseModel):
    event_id: int

@app.on_event("startup")
def startup():
    init_db()

@app.post("/recommend")
def recommend(req: RecommendRequest):
    # Get features
    features = get_user_features(req.user_id)
    # Route to model
    if random.random() < CHAMPION_WEIGHT:
        model = model_champion
        version = "champion"
    else:
        model = model_challenger
        version = "challenger"

    # Prepare input
    X = pd.DataFrame([features])
    prediction = model.predict(X)[0]
    PREDICTION_COUNT.labels(model_version=version).inc()

    # Log to feedback DB
    event_id = log_prediction(req.user_id, version, prediction)

    return {"recommendation_score": prediction, "model_version": version, "event_id": event_id}

@app.post("/click")
def click(req: ClickRequest):
    log_click(req.event_id)
    CLICK_COUNT.labels(model_version="unknown").inc()  # In real system you'd know version
    return {"status": "click recorded"}

@app.get("/metrics")
def metrics():
    return generate_latest()

@app.get("/ctr")
def ctr():
    return get_ctr()