import streamlit as st
import pandas as pd
import joblib
import os
import numpy as np
import plotly.graph_objects as go

# --------------------------------------------------------
# ACCESS PROTECTION
# --------------------------------------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("❌ Access denied. Please log in first.")
    st.stop()

st.title("🔍 Predict Pump Health Status")

# --------------------------------------------------------
# FIXED PATHS
# --------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))     # /pages
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
MODEL_DIR = os.path.join(PROJECT_DIR, "model")

MODEL_PATH = os.path.join(MODEL_DIR, "trained_model_xgb.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler2.pkl")

# --------------------------------------------------------
# Load model & scaler
# --------------------------------------------------------
if not os.path.exists(MODEL_PATH):
    st.error(f"❌ Model file missing: {MODEL_PATH}")
    st.stop()

if not os.path.exists(SCALER_PATH):
    st.error(f"❌ Scaler file missing: {SCALER_PATH}")
    st.stop()

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
st.success("✅ Model & scaler loaded successfully.")

# --------------------------------------------------------
# Check for uploaded data
# --------------------------------------------------------
if "uploaded_df" not in st.session_state:
    st.warning("⚠ Please upload data first.")
    st.stop()

df = st.session_state.uploaded_df.copy()

st.subheader("📄 Uploaded Data Preview")
st.dataframe(df.head())

# --------------------------------------------------------
# Required columns
# --------------------------------------------------------
REQUIRED_COLS = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]"
]

missing = [c for c in REQUIRED_COLS if c not in df.columns]

if missing:
    st.error(f"❌ Missing required columns: {missing}")
    st.stop()

# --------------------------------------------------------
# Prepare features
# --------------------------------------------------------
X = df[REQUIRED_COLS]

try:
    X_scaled = scaler.transform(X)
except Exception as e:
    st.error(f"❌ Scaler error: {e}")
    st.stop()

# ========================================================
# RUN PREDICTION BUTTON
# ========================================================
if st.button("🔍 Run Prediction"):

    # --------------------------------------------------------
    # Make predictions
    # --------------------------------------------------------
    pred = model.predict(X_scaled)
    prob = model.predict_proba(X_scaled)[:, 1]

    df_result = df.copy()
    df_result["Failure Probability"] = prob
    df_result["Predicted Label"] = pred
    df_result["Health Status"] = [
        "🔴 CRITICAL" if p > 0.8 else
        "🟠 WARNING" if p > 0.4 else
        "🟢 NORMAL"
        for p in prob
    ]

    # --------------------------------------------------------
    # Initialize logs if needed
    # --------------------------------------------------------
    if "logs" not in st.session_state or not isinstance(st.session_state.logs, pd.DataFrame):
        st.session_state.logs = pd.DataFrame()

    # --------------------------------------------------------
    # Append new results to historical logs
    # --------------------------------------------------------
    df_result.reset_index(drop=True, inplace=True)
    st.session_state.logs = pd.concat(
        [st.session_state.logs, df_result],
        ignore_index=True
    )

    # Save the latest prediction batch
    st.session_state.df_result = df_result

    # --------------------------------------------------------
    # Show Prediction Table
    # --------------------------------------------------------
    st.subheader("📊 Prediction Results")
    st.dataframe(df_result)

    # --------------------------------------------------------
    # Gauge Meter
    # --------------------------------------------------------
    st.subheader("⏱ Failure Probability Gauge")

    avg_prob = float(np.mean(prob)) * 100

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_prob,
        title={'text': "Failure Risk (%)"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkred"},
            'steps': [
                {'range': [0, 40], 'color': "green"},
                {'range': [40, 80], 'color': "orange"},
                {'range': [80, 100], 'color': "red"}
            ],
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------
    st.subheader("📊 Summary Report")

    failures = (pred == 1).sum()
    normals = (pred == 0).sum()

    col1, col2 = st.columns(2)
    col1.metric("Normal Equipment", normals)
    col2.metric("Predicted Failures", failures)

    if failures > 0:
        st.error("⚠️ ALERT: Potential pump failure detected!")
    else:
        st.success("✔ Pump operating normally.")
