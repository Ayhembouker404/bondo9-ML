# app/model_loader.py
import joblib
from functools import lru_cache

@lru_cache(maxsize=1)
def load_model():
    # This only runs once, then saves the result in memory
    print("Loading model into memory...")
    return joblib.load("models/model.joblib")
