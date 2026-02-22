# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()
model = joblib.load("models/model.joblib")

class Features(BaseModel):
    data: list[float]  # Expecting a list of 28 floats

@app.get("/health")
def health_check():
    return {"status": "healthy", "features_required": 28}

@app.post("/predict")
def predict(features: Features):
    if len(features.data) != 28:
        return {"error": f"Expected 28 features, got {len(features.data)}"}
    
    prediction = model.predict([features.data])
    return {"prediction": int(prediction[0])}
