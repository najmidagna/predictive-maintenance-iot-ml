import streamlit as st
import pandas as pd
import joblib
import os
import numpy as np

st.title("🔍 Predict Pump Health Status")

# --------------------------------------------------------
# Load trained model & scaler
# --------------------------------------------------------
MODEL_PATH = "model/trained_model_xgb.pkl"
SCALER_PATH = "model/scaler.pkl"

if not os.path.exists(MODEL_PATH):
    st.error("❌ Model file missing! Train the model first.")
    st.stop()

if not os.path.exists(SCALER_PATH):
    st.error("❌ Scaler file missing! Train the model first.")
    st.stop()

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
st.success("✅ Model & scaler loaded successfully.")

# --------------------------------------------------------
# Ensure data was uploaded earlier
# --------------------------------------------------------
if "uploaded_df" not in st.session_state:
    st.warning("⚠ Upload data first using the 'Upload Data' page.")
    st.stop()

df = st.session_state.uploaded_df

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
# Prepare data for prediction
# --------------------------------------------------------
X = df[REQUIRED_COLS]

try:
    X_scaled = scaler.transform(X)
except Exception as e:
    st.error(f"Scaler error: {e}")
    st.stop()

# --------------------------------------------------------
# RUN PREDICTION
# --------------------------------------------------------
pred = model.predict(X_scaled)
prob = model.predict_proba(X_scaled)[:, 1]   # probability of failure

df_result = df.copy()
df_result["Failure Probability"] = prob
df_result["Predicted Label"] = pred
df_result["Health Status"] = df_result["Failure Probability"].apply(
    lambda p: "🔴 CRITICAL" if p > 0.8 else ("🟠 WARNING" if p > 0.4 else "🟢 NORMAL")
)

st.subheader("📊 Prediction Results")
st.dataframe(df_result)

# --------------------------------------------------------
# SUMMARY
# --------------------------------------------------------
st.subheader("📊 Summary Report")

failures = (pred == 1).sum()
normals = (pred == 0).sum()

colA, colB = st.columns(2)

with colA:
    st.metric("Normal Equipment", normals)

with colB:
    st.metric("Predicted Failures", failures)

# --------------------------------------------------------
# ALERT
# --------------------------------------------------------
if failures > 0:
    st.error("⚠️ ALERT: Potential equipment failure detected!")
else:
    st.success("✔ All equipment are operating normally.")
