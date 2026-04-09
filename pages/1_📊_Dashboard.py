import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sidebar import show_sidebar
from footer import show_footer


st.set_page_config(
    page_title="Predictive Maintenance System",
    page_icon="🛠️",
    layout="wide"
)

show_sidebar()
# --------------------------------------------------------
# ACCESS PROTECTION
# --------------------------------------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("❌ Access denied. Please log in first.")
    st.stop()

st.title("📊 Equipment Health Dashboard")

# ----------------------------------------------------------
# Check if data exists
# ----------------------------------------------------------
if "uploaded_df" not in st.session_state:
    st.warning("⚠ No uploaded data found. Please upload IoT sensor data first.")
    st.stop()

df = st.session_state.uploaded_df.copy()

if df.empty:
    st.warning("⚠ Uploaded data is empty.")
    st.stop()

# Required columns
REQUIRED_COLS = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]"
]

missing = [c for c in REQUIRED_COLS if c not in df.columns]
if missing:
    st.error(f"❌ Dashboard error: Missing required columns: {missing}")
    st.stop()

# If prediction page already generated results, include them
if "Predicted Label" in df.columns:
    labels_available = True
else:
    labels_available = False


# ----------------------------------------------------------
# KPI SUMMARY
# ----------------------------------------------------------
st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Samples", len(df))
col2.metric("Avg Air Temp (K)", f"{df['Air temperature [K]'].mean():.1f}")
col3.metric("Avg Torque (Nm)", f"{df['Torque [Nm]'].mean():.1f}")
col4.metric("Avg RPM", f"{df['Rotational speed [rpm]'].mean():.0f}")
col5.metric("Avg Tool Wear (min)", f"{df['Tool wear [min]'].mean():.1f}")

# If predictions exist, show health counts
if labels_available:
    failures = df["Predicted Label"].sum()
    normals = len(df) - failures

    st.success(f"Health Summary → 🟢 {normals} Normal | 🔴 {failures} Failures")


# ----------------------------------------------------------
# LINE CHARTS SECTION
# ----------------------------------------------------------
st.subheader("📈 Sensor Trends Over Time")

for col in REQUIRED_COLS:
    fig = px.line(df, y=col, title=f"{col} Trend")
    st.plotly_chart(fig, use_container_width=True)


# ----------------------------------------------------------
# IF PREDICTIONS EXIST → ADD ADVANCED VISUALS
# ----------------------------------------------------------
if labels_available:

    st.subheader("🎯 Failure Probability Distribution")
    fig = px.histogram(df, x="Failure Probability", nbins=20,
                       title="Failure Probability Distribution",
                       color="Health Status")
    st.plotly_chart(fig, use_container_width=True)

    # Pie chart
    st.subheader("🛠 Equipment Health Status")
    fig2 = px.pie(
        df,
        names="Health Status",
        title="Health Status Distribution",
        color="Health Status",
        color_discrete_map={
            "🟢 NORMAL": "green",
            "🟠 WARNING": "orange",
            "🔴 CRITICAL": "red"
        }
    )
    st.plotly_chart(fig2, use_container_width=True)


# ----------------------------------------------------------
# RAW DATA VIEWER
# ----------------------------------------------------------
st.subheader("📄 Raw Data")
st.dataframe(df)

show_footer()
