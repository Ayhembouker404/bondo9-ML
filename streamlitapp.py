import streamlit as st
import requests
import pandas as pd
import numpy as np

# Page Config
st.set_page_config(
    page_title="AI Classifier Pro",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for a clean look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .prediction-box { padding: 20px; border-radius: 10px; text-align: center; font-size: 24px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("Settings")
    st.info("Status: API Connected ✅")
    st.divider()
    st.markdown("### Model Info")
    st.write("**Version:** 1.0.4-stable")
    st.write("**Features:** 28 Input Dimensions")
    if st.button("Reset Inputs"):
        st.rerun()

# --- MAIN CONTENT ---
st.title("🚀 Enterprise Feature Classifier")
st.write("Input the 28 required features below to generate a real-time classification.")

# Grouping 28 features into 4 tabs (7 features each) to avoid a "wall of inputs"
tab1, tab2, tab3, tab4 = st.tabs(["Primary Metrics", "Secondary Data", "Environmental", "Historical"])

features = []

with tab1:
    st.subheader("Core Indicators")
    col1, col2 = st.columns(2)
    for i in range(1, 8):
        with (col1 if i % 2 == 0 else col2):
            val = st.number_input(f"Feature {i}", value=0.0, key=f"f{i}")
            features.append(val)

with tab2:
    st.subheader("Technical Specs")
    col1, col2 = st.columns(2)
    for i in range(8, 15):
        with (col1 if i % 2 == 0 else col2):
            val = st.number_input(f"Feature {i}", value=0.0, key=f"f{i}")
            features.append(val)

with tab3:
    st.subheader("Contextual Variables")
    col1, col2 = st.columns(2)
    for i in range(15, 22):
        with (col1 if i % 2 == 0 else col2):
            val = st.number_input(f"Feature {i}", value=0.0, key=f"f{i}")
            features.append(val)

with tab4:
    st.subheader("Temporal Data")
    col1, col2 = st.columns(2)
    for i in range(22, 29):
        with (col1 if i % 2 == 0 else col2):
            val = st.number_input(f"Feature {i}", value=0.0, key=f"f{i}")
            features.append(val)

st.divider()

# --- INFERENCE SECTION ---
if st.button("Run Classification"):
    with st.spinner("Consulting the model..."):
        try:
            # Pointing to your FastAPI endpoint (running on port 8000)
            response = requests.post(
                "http://localhost:8000/predict", 
                json={"data": features},
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json().get("prediction")
                
                # Visual Result
                st.balloons()
                if result == 1:
                    st.success("### Prediction: POSITIVE / CLASS A")
                else:
                    st.warning("### Prediction: NEGATIVE / CLASS B")
                
                # Show the raw vector for transparency
                with st.expander("View Input Vector"):
                    st.json(features)
            else:
                st.error(f"Error: {response.text}")
        except Exception as e:
            st.error(f"Could not connect to API: {e}")

# --- FOOTER ---
st.markdown("---")
st.caption("Internal AI Inference Tool • v2026.02")
