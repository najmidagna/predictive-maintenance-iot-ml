import streamlit as st
import joblib
import numpy as np
import os
from sidebar import show_sidebar
from footer import show_footer


st.set_page_config(
    page_title="Predictive Maintenance System",
    page_icon="🛠️",
    layout="wide"
)

show_sidebar()
# -----------------------------------------------------
# ACCESS CONTROL
# -----------------------------------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("❌ Please log in first.")
    st.stop()

st.title("⚡ Instant Pump Health Check (No Upload Needed)")

# -----------------------------------------------------
# LOAD MODEL & SCALER WITH SAFE PATH
# -----------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
MODEL_DIR = os.path.join(PROJECT_DIR, "model")

MODEL_PATH = os.path.join(MODEL_DIR, "trained_model_xgb.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler2.pkl")

if not os.path.exists(MODEL_PATH):
    st.error(f"❌ Model missing: {MODEL_PATH}")
    st.stop()

if not os.path.exists(SCALER_PATH):
    st.error(f"❌ Scaler missing: {SCALER_PATH}")
    st.stop()

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# -----------------------------------------------------
# USER INPUTS FOR INSTANT CHECK
# -----------------------------------------------------
st.subheader("📥 Enter Sensor Values Manually")

col1, col2 = st.columns(2)

with col1:
    air_temp = st.number_input(
        "Air Temperature [K]",
        min_value=250.0,
        max_value=500.0,
        value=300.0,
        step=10.0   # ✅ change step
    )

    rpm = st.number_input(
        "Rotational Speed [rpm]",
        min_value=0,
        max_value=5000,
        value=1500,
        step=100    # ✅ better for rpm
    )

with col2:
    proc_temp = st.number_input(
        "Process Temperature [K]",
        min_value=250.0,
        max_value=800.0,
        value=350.0,
        step=10.0   # ✅ change step
    )

    torque = st.number_input(
        "Torque [Nm]",
        min_value=0.0,
        max_value=200.0,
        value=30.0,
        step=10.0   # ✅ change step
    )

tool_wear = st.number_input(
    "Tool Wear [min]",
    min_value=0,
    max_value=500,
    value=10,
    step=10   # ✅ change step
)
# -----------------------------------------------------
# RUN PREDICTION
# -----------------------------------------------------
if st.button("🔍 Check Health Now"):
    input_data = np.array([[air_temp, proc_temp, rpm, torque, tool_wear]])

    # Scale
    try:
        scaled = scaler.transform(input_data)
    except Exception as e:
        st.error(f"Scaler error: {e}")
        st.stop()

    # Predict
    pred = model.predict(scaled)[0]
    prob = model.predict_proba(scaled)[0][1]

    # Determine status
    if prob > 0.8:
        status = "🔴 CRITICAL — Immediate Maintenance Required"
    elif prob > 0.4:
        status = "🟠 WARNING — Monitor Closely"
    else:
        status = "🟢 NORMAL — Pump is Operating Normally"

    # Output
    st.subheader("📊 Instant Prediction Result")
    st.write(f"### Failure Probability: **{prob:.2f}**")
    st.write(f"### Health Status: {status}")

show_footer()
