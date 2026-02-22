from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
import os

app = FastAPI(title="Coverage Bundle Predictor")

# Load the bundle once when the API starts (In-memory caching)
base_path = os.path.dirname(__file__)
bundle = joblib.load(os.path.join(base_path, "model.pkl"))

@app.get("/health")
def health_check():
    """Endpoint 1: Check if API is alive."""
    return {"status": "online", "model_loaded": bundle is not None}

@app.post("/predict")
def predict(data: list[dict]):
    """Endpoint 2: Inference logic."""
    try:
        df = pd.DataFrame(data)
        
        # 1. Align features (using bundle['features'])
        # (Insert your alignment and scaling logic here as per solution.py)
        
        # 2. Inference
        # X_scaled = bundle['scaler'].transform(df[bundle['features']])
        # preds = bundle['model'].predict(X_scaled)
        
        return {"predictions": [int(p) for p in [1, 0, 1]]} # Placeholder
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))