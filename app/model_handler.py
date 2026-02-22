import joblib
import numpy as np

class ModelHandler:
    def __init__(self, model_path="models/model.pkl"):
        # For this demo, we'll simulate a model if the file doesn't exist
        try:
            self.model = joblib.load(model_path)
        except:
            self.model = None

    def predict(self, data: list):
        if self.model:
            return self.model.predict([data])[0]
        # Fallback dummy logic: sum the inputs
        return sum(data)
