import streamlit as st
import pandas as pd

# --------------------------------------------------------
# ACCESS CONTROL
# --------------------------------------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("❌ Access denied. Please log in first.")
    st.stop()

# --------------------------------------------------------
# HOME PAGE TITLE
# --------------------------------------------------------
st.title("🏠 Home Page")
st.write(f"👋 Welcome, **{st.session_state.username}**!")
st.write(f"**Role:** {st.session_state.role.capitalize()}")

st.markdown("---")

# --------------------------------------------------------
# QUICK NAVIGATION SECTION
# --------------------------------------------------------
st.subheader("📌 Quick Navigation")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📁 Upload Sensor Data"):
        st.switch_page("pages/2_Upload_Data.py")

    if st.button("⚡ Instant Health Check"):
        st.switch_page("pages/6_Instant_Health_Check.py")

with col2:
    if st.button("🔍 Predict Health"):
        st.switch_page("pages/3_Predict_Health.py")

    if st.button("📘 Detailed Log"):
        st.switch_page("pages/4_Detailed_Log.py")

with col3:
    if st.button("📊 Dashboard"):
        st.switch_page("pages/1_Dashboard.py")

    if st.button("⬇ Download Report"):
        st.switch_page("pages/5_Download_Report.py")

st.markdown("---")

# --------------------------------------------------------
# SYSTEM OVERVIEW
# --------------------------------------------------------
st.subheader("🛢 About This System")
st.write("""
This Predictive Maintenance System analyzes pump sensor data—including temperature, 
RPM, torque, and wear—to estimate failure probability using a machine learning model.

**Key Features:**
- Real-time pump health prediction  
- Failure risk gauge visualization  
- Predictive maintenance dashboard  
- Manual instant health check  
- Detailed equipment log history  
- Multi-user login system (Admin/User)  
- Report download and data analysis  
""")

st.markdown("---")

# --------------------------------------------------------
# LATEST PREDICTION SUMMARY
# --------------------------------------------------------
st.subheader("📊 Latest Prediction Summary")

if "df_result" in st.session_state and st.session_state.df_result is not None:
    df = st.session_state.df_result

    try:
        latest_status = df["Health Status"].iloc[-1]
        latest_prob = df["Failure Probability"].iloc[-1]

        colA, colB = st.columns(2)
        colA.metric("Latest Health Status", latest_status)
        colB.metric("Failure Probability", f"{latest_prob:.2f}")

    except Exception:
        st.warning("⚠ Latest prediction could not be loaded. Run a new prediction.")

else:
    st.info("No prediction available yet. Upload data and perform prediction.")

st.markdown("---")

# --------------------------------------------------------
# ADDITIONAL SECTION (OPTIONAL)
# --------------------------------------------------------
st.subheader("📄 Tips for Using the System")
st.write("""
- Begin by uploading pump sensor data using the *Upload Data* page.  
- Then run the *Predict Health* module to generate predictions.  
- View long-term analytics in the *Dashboard* and *Detailed Log* pages.  
- Use *Instant Health Check* to test data manually without uploading files.  
""")

st.markdown("---")

# --------------------------------------------------------
# FOOTER / LOGOUT BUTTON
# --------------------------------------------------------
if st.sidebar.button("Log Out"):
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.df_result = None
    st.session_state.logs = None
    st.rerun()
