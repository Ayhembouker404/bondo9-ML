import streamlit as st
import requests

st.title("Bundle Prediction Interface")

# User Inputs
income = st.number_input("Annual Income", min_value=0)
age = st.slider("User Age", 18, 100, 30)

if st.button("Predict Bundle"):
    payload = [{"Estimated_Annual_Income": income, "Age": age}]
    response = requests.post("http://localhost:8000/predict", json=payload)
    
    if response.status_code == 200:
        result = response.json()["predictions"]
        st.success(f"Recommended Bundle: {result[0]}")
    else:
        st.error("Prediction failed.")