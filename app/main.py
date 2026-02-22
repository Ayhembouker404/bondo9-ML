from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# Load your model (ensure it's trained on these 28 features)
model = joblib.load("model.pkl")

class PolicyFeatures(BaseModel):
    User_ID: str
    Policy_Start_Year: int
    Policy_Start_Week: int
    Policy_Start_Day: int
    Grace_Period_Extensions: int
    Previous_Policy_Duration_Months: int
    Adult_Dependents: int
    Child_Dependents: float
    Infant_Dependents: int
    Region_Code: str
    Existing_Policyholder: int
    Previous_Claims_Filed: int
    Years_Without_Claims: int
    Policy_Amendments_Count: int
    Broker_ID: float
    Employer_ID: float
    Underwriting_Processing_Days: int
    Vehicles_on_Policy: int
    Custom_Riders_Requested: int
    Broker_Agency_Type: str
    Deductible_Tier: str
    Acquisition_Channel: str
    Payment_Schedule: str
    Employment_Status: str
    Estimated_Annual_Income: float
    Days_Since_Quote: int
    Policy_Start_Month: str
    Purchased_Coverage_Bundle: int

@app.get("/health")
def health():
    return {"status": "online", "model": "Policy_Cancellation_Classifier_v1"}

@app.post("/predict")
def predict(data: PolicyFeatures):
    # Convert Pydantic model to DataFrame for the model
    input_df = pd.DataFrame([data.dict()])
    
    # Preprocessing logic (Encoding strings) would go here
    prediction = model.predict(input_df)
    
    # Mock response for testing
    return {"prediction": 0, "probability": 0.12, "User_ID": data.User_ID}

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, replace "*" with your streamlit URL
    allow_methods=["*"],
    allow_headers=["*"],
)
