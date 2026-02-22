import streamlit as st
import requests

st.set_page_config(page_title="Policy Risk Analyzer", page_icon="🛡️", layout="wide")

st.title("🛡️ Policy Cancellation Risk Predictor")
st.markdown("Enter policy details below to evaluate the cancellation probability.")

# Define Options from train.csv
REGIONS = ["AUT", "PRT", "FRA", "IRL", "GBR", "ESP", "BEL", "ITA", "USA", "DEU"]
CHANNELS = ["Aggregator_Site", "Direct_Website", "Affiliate_Group", "Corporate_Partner", "Local_Broker"]
TIERS = ["Tier_1_High_Ded", "Tier_2_Mid_Ded", "Tier_3_Low_Ded", "Tier_4_Zero_Ded"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

with st.expander("ℹ️ Instructions", expanded=False):
    st.write("Fill out all 4 tabs of information. The model uses 28 specific features to calculate risk.")

# Organize 28 features into 4 logical tabs
tab1, tab2, tab3, tab4 = st.tabs(["👤 Client Profile", "📅 Policy Timing", "💼 Broker & Agent", "📜 Coverage Details"])

inputs = {}

with tab1:
    col1, col2 = st.columns(2)
    inputs["User_ID"] = col1.text_input("User ID", "USR_000000")
    inputs["Employment_Status"] = col2.selectbox("Employment Status", ["Employed_FullTime", "Self_Employed", "Contractor", "Unemployed"])
    inputs["Estimated_Annual_Income"] = col1.number_input("Annual Income ($)", min_value=0.0, value=35000.0)
    inputs["Adult_Dependents"] = col2.slider("Adult Dependents", 0, 10, 2)
    inputs["Child_Dependents"] = col1.slider("Child Dependents", 0, 10, 0)
    inputs["Infant_Dependents"] = col2.slider("Infant Dependents", 0, 5, 0)
    inputs["Existing_Policyholder"] = col1.radio("Existing Customer?", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")

with tab2:
    col1, col2 = st.columns(2)
    inputs["Policy_Start_Year"] = col1.selectbox("Start Year", [2015, 2016, 2017])
    inputs["Policy_Start_Month"] = col2.selectbox("Start Month", MONTHS)
    inputs["Policy_Start_Week"] = col1.number_input("Start Week", 1, 53, 10)
    inputs["Policy_Start_Day"] = col2.number_input("Start Day", 1, 31, 15)
    inputs["Days_Since_Quote"] = col1.number_input("Days Since Quote", 0, 500, 30)
    inputs["Underwriting_Processing_Days"] = col2.number_input("Underwriting Days", 0, 400, 0)
    inputs["Region_Code"] = col1.selectbox("Region Code", REGIONS)

with tab3:
    col1, col2 = st.columns(2)
    inputs["Broker_ID"] = col1.number_input("Broker ID", value=250.0)
    inputs["Employer_ID"] = col2.number_input("Employer ID (Optional)", value=0.0)
    inputs["Broker_Agency_Type"] = col1.selectbox("Agency Type", ["Urban_Boutique", "National_Corporate"])
    inputs["Acquisition_Channel"] = col2.selectbox("Acquisition Channel", CHANNELS)
    inputs["Previous_Claims_Filed"] = col1.number_input("Previous Claims", 0, 50, 0)
    inputs["Years_Without_Claims"] = col2.number_input("Years Without Claims", 0, 100, 0)
    inputs["Previous_Policy_Duration_Months"] = col1.number_input("Prev Policy Duration (Months)", 0, 100, 0)

with tab4:
    col1, col2 = st.columns(2)
    inputs["Deductible_Tier"] = col1.selectbox("Deductible Tier", TIERS)
    inputs["Payment_Schedule"] = col2.selectbox("Payment Schedule", ["Monthly_EFT", "Annual_Upfront", "Quarterly_Invoice"])
    inputs["Purchased_Coverage_Bundle"] = col1.slider("Coverage Bundle Level", 0, 10, 2)
    inputs["Vehicles_on_Policy"] = col2.slider("Vehicles", 0, 10, 1)
    inputs["Policy_Amendments_Count"] = col1.number_input("Policy Amendments", 0, 20, 0)
    inputs["Custom_Riders_Requested"] = col2.number_input("Custom Riders", 0, 10, 0)
    inputs["Grace_Period_Extensions"] = col1.number_input("Grace Period Extensions", 0, 20, 0)

st.divider()

if st.button("🔍 Run Risk Analysis", type="primary"):
    if not api_url:
        st.error("❌ Configuration Error: 'BACKEND_URL' not found in Streamlit Secrets.")
    else:
        with st.spinner("Connecting to Render API..."):
            try:
                # Ensure 'inputs' is the dictionary of your 28 features
                response = requests.post(
                    f"{api_url.rstrip('/')}/predict", 
                    json=inputs,
                    timeout=20 # Render "Free Tier" spins down; needs time to wake up
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"Analysis Complete for {result['User_ID']}")
                    st.metric("Cancellation Prediction", result['prediction'])
                else:
                    st.error(f"API Error ({response.status_code}): {response.text}")
                    
            except requests.exceptions.ConnectTimeout:
                st.error("⏳ Connection Timeout. The Render free tier might be 'waking up'. Please try again in 30 seconds.")
            except Exception as e:
                st.error(f"📡 Connection Failed: {e}")
