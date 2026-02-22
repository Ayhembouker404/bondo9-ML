# app/ui.py
import streamlit as st
import requests

st.title("AI Classifier (28 Features)")

# Option to input data
input_data = st.text_area("Paste 28 comma-separated features:", "0,1,2...")

if st.button("Classify"):
    feature_list = [float(x) for x in input_data.split(",")]
    response = requests.post("http://localhost:8000/predict", json={"data": feature_list})
    st.write(f"Result: {response.json()}")
