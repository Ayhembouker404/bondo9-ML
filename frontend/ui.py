import streamlit as st
import requests

st.title("🚀 ML Model Predictor")

# UI Inputs
val1 = st.number_input("Enter Feature 1", value=0.0)
val2 = st.number_input("Enter Feature 2", value=0.0)

if st.button("Get Prediction"):
    payload = {"features": [val1, val2]}
    
    # Replace URL with your live URL after deployment
    response = requests.post("http://localhost:8000/predict", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        st.success(f"The model predicted: {result['prediction']}")
    else:
        st.error("Failed to connect to the API.")
