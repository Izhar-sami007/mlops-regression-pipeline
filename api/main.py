
from __future__ import annotations
from pathlib import Path
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, conlist
import joblib

MODELS_DIR = Path(__file__).resolve().parents[1] / "models"
MODEL_PATH = MODELS_DIR / "regressor.joblib"

class InputData(BaseModel):
    # Accept 2+ features to avoid over-constraining; adjust for your use case
    features: conlist(float, min_items=2) = Field(..., description="List of feature values")

app = FastAPI(title="Regression API", version="1.0")

def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Train first.")
    return joblib.load(MODEL_PATH)

model = load_model()

@app.get("/")
def root():
    return {"status": "ok", "message": "Regression API running"}

@app.post("/predict")
def predict(data: InputData):
    try:
        arr = np.array([data.features], dtype=float)
        pred = model.predict(arr)[0]
        return {"prediction": float(pred)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")
