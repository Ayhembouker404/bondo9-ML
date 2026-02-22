import pandas as pd
import numpy as np
import joblib
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Initialize FastAPI
app = FastAPI(title="ML Inference API")

# --- PATH SAFETY LOGIC ---
# This ensures the API finds model.pkl regardless of where it's running
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

# Global variable to hold our bundle
bundle = None

@app.on_event("startup")
def load_bundle():
    global bundle
    if not os.path.exists(MODEL_PATH):
        print(f"ERROR: {MODEL_PATH} not found!")
        # We don't crash the whole app immediately so we can return a 500 error later
        bundle = None
    else:
        bundle = joblib.load(MODEL_PATH)
        print("Model bundle loaded successfully.")

# --- DATA MODELS ---
class InferenceInput(BaseModel):
    # Update these fields to match your CSV columns
    User_ID: str
    Estimated_Annual_Income: float
    Age: int
    # Add other necessary columns here...

# --- ENDPOINTS ---

# 1. Health Check Endpoint
@app.get("/health")
def health():
    if bundle is None:
        return {"status": "error", "message": f"model.pkl missing at {MODEL_PATH}"}
    return {"status": "healthy", "model_info": "Logistic Regression Bundle Loaded"}

# 2. Prediction Endpoint
@app.post("/predict")
def predict(inputs: List[dict]):
    global bundle
    if bundle is None:
        raise HTTPException(status_code=500, detail="Model not loaded on server.")

    try:
        # Convert incoming JSON to DataFrame
        df = pd.DataFrame(inputs)
        user_ids = df['User_ID']

        # --- PREPROCESSING ---
        # 1. Fill Missing
        df = df.fillna(0)
        
        # 2. Categorical Encoding (get_dummies)
        df_encoded = pd.get_dummies(df)

        # 3. Align Columns
        expected_features = bundle['features']
        for col in expected_features:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
        
        X = df_encoded[expected_features]

        # 4. Scale and Predict
        X_scaled = bundle['scaler'].transform(X)
        preds = bundle['model'].predict(X_scaled)

        # 5. Return JSON
        results = []
        for uid, pred in zip(user_ids, preds):
            results.append({"User_ID": uid, "Purchased_Coverage_Bundle": int(pred)})
        
        return {"predictions": results}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
