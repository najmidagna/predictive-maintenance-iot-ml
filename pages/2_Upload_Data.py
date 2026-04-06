import streamlit as st
import pandas as pd
# --------------------------------------------------------
# ACCESS PROTECTION
# --------------------------------------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("❌ Access denied. Please log in first.")
    st.stop()

st.title("📁 Upload IoT Sensor Data")
st.write("Upload a CSV file containing machine sensor readings for predictive health analysis.")

# ---------------------------------------------------------
# FILE UPLOADER
# ---------------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"],
    help="File must include: Air Temp, Process Temp, RPM, Torque, Tool Wear"
)

# Expected columns for your ML model
REQUIRED_COLS = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]"
]

# ---------------------------------------------------------
# PROCESS UPLOADED FILE
# ---------------------------------------------------------
if uploaded_file:

    try:
        df = pd.read_csv(uploaded_file)

        st.write("### 📄 Data Preview")
        st.dataframe(df.head())

        # Store uploaded data globally
        st.session_state.uploaded_df = df

        # -------------------------------------------
        # Column validation
        # -------------------------------------------
        missing_cols = [c for c in REQUIRED_COLS if c not in df.columns]

        if missing_cols:
            st.error(f"❌ Missing required columns: {missing_cols}")
            st.stop()

        st.success("✅ File uploaded and validated successfully!")

        # -------------------------------------------
        # Convert numeric fields safely
        # -------------------------------------------
        try:
            df[REQUIRED_COLS] = df[REQUIRED_COLS].apply(pd.to_numeric, errors="raise")
            st.success("🔧 Numeric validation passed.")
        except Exception:
            st.error("❌ Non-numeric data found in required columns.")
            st.stop()

        # Save cleaned data
        st.session_state.uploaded_df = df

        st.info("Go to the **Predict Health** page to run predictions.")

    except Exception as e:
        st.error("❌ Error reading CSV file.")
        st.error(str(e))

else:
    st.info("📌 Please upload a CSV file to continue.")
