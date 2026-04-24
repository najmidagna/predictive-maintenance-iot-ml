import streamlit as st
import pandas as pd
import datetime
from sidebar import show_sidebar
from footer import show_footer

show_sidebar() 
# --------------------------------------------------------
# ACCESS CONTROL
# --------------------------------------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("❌ Access denied. Please log in first.")
    st.stop()
# --------------------------------------------------------
# CUSTOM DARK MODE + GRADIENT STYLING
# --------------------------------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f0f0f, #1e1e1e);
    color: white !important;
}

            
.main-title {
    font-size: 60px;
    font-weight: bold;
    color: "white";
    margin-bottom: 10px;
    text-shadow: 0px 0px 8px rgba(76, 175, 80, 0.6);
}

/* Adaptive box */
.welcome-box {
    padding: 15px;
    border-radius: 10px;
    border-left: 5px solid #4CAF50;
    margin-bottom: 15px;
    backdrop-filter: blur(10px);

    background-color: rgba(255, 255, 255, 0.05); /* works for dark */
}

/* Adaptive text */
.system-desc {
    font-size: 15px;
    opacity: 0.9;
}

/* Optional: make everything smoother */
div[data-testid="stMarkdownContainer"] {
    color: inherit;
}
.feature-card {
    background-color: rgba(255,255,255,0.05);
    border: 1px solid #2a2a2a;
    border-radius: 10px;
    padding: 15px;
    text-align: center;
    transition: 0.2s ease;
}
.feature-card:hover {
    background-color: rgba(255,255,255,0.15);
    box-shadow: 0 0 12px rgba(0, 180, 255, 0.4);
    transform: translateY(-4px);
}
.footer {
    color:#bbb;
    font-size: 13px;
    text-align: center;
    margin-top: 3rem;
}
/* Target all Streamlit buttons */
div.stButton > button {
    background-color: #f0f2f6;
    color: black;
    border-radius: 10px;
    padding: 10px 15px;
    border: 1px solid #ccc;
    transition: all 0.3s ease;
}

/* Hover effect */
div.stButton > button:hover {
    background-color: #4CAF50;
    color: white;
    border: 1px solid #4CAF50;
    transform: scale(1.05);
    cursor: pointer;
}

/* Optional: Active click effect */
div.stButton > button:active {
    transform: scale(0.98);
}

</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Predictive Maintenance System",
    page_icon="🛠️",
    layout="wide"
)



# --------------------------------------------------------
# HEADER/WELCOME SECTION
# --------------------------------------------------------
st.markdown('<div class="main-title">🛠️ Predictive Maintenance System</div>', unsafe_allow_html=True)

st.markdown(
    f"""
    <div class='welcome-box'>
        👋 Welcome, <b>{st.session_state.username}</b> 
        ({st.session_state.role.capitalize()})<br>
        📅 {datetime.datetime.now().strftime('%d %B %Y • %H:%M')}
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='system-desc'>
    This system monitors oil and gas equipment using IoT sensor data and 
    machine learning models to predict potential failures early, reducing 
    downtime and improving operational safety.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")
# --------------------------------------------------------
# QUICK NAVIGATION SECTION
# --------------------------------------------------------
st.subheader("📌 Quick Navigation")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📁 Upload Sensor Data"):
        st.switch_page("pages/2_📁_Upload_Data.py")

    if st.button("⚡ Instant Health Check"):
        st.switch_page("pages/4_⚡_Instant_Health_Check.py")

with col2:
    if st.button("🔍 Predict Health"):
        st.switch_page("pages/3_🔍_Predict_Health.py")

    if st.button("📘 Detailed Log"):
        st.switch_page("pages/5_📘_Detailed_Log.py")

with col3:
    if st.button("📊 Dashboard"):
        st.switch_page("pages/1_📊_Dashboard.py")

    if st.button("⬇ Download Report"):
        st.switch_page("pages/6_📄_Download_Report.py")

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

show_footer() 
