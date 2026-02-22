from fastapi import FastAPI
from pydantic import BaseModel
from .model_handler import ModelHandler

app = FastAPI(title="ML Inference API")
handler = ModelHandler()

# Data validation schema
class InferenceInput(BaseModel):
    features: list[float]

# Endpoint 1: Health Check (Requirement)
@app.get("/")
def health_check():
    return {"status": "online", "model_loaded": handler.model is not None}

# Endpoint 2: Prediction (Requirement)
@app.post("/predict")
def predict(input_data: InferenceInput):
    prediction = handler.predict(input_data.features)
    return {"prediction": prediction}
