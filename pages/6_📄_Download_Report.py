import streamlit as st
import pandas as pd
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
    st.error("❌ Please log in first.")
    st.stop()

st.title("📄 Download Report")

# --------------------------------------------------------
# CHECK IF PREDICTION RESULTS EXIST
# --------------------------------------------------------
if "df_result" not in st.session_state or st.session_state.df_result is None:
    st.warning("⚠ No prediction data found.")
    st.info("Please run prediction first in the 'Predict Health' page.")
    st.stop()

df = st.session_state.df_result

# --------------------------------------------------------
# SHOW PREVIEW
# --------------------------------------------------------
st.subheader("📊 Report Preview")
st.dataframe(df, use_container_width=True)

# --------------------------------------------------------
# DOWNLOAD CSV
# --------------------------------------------------------
st.subheader("⬇ Download CSV Report")

csv_data = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Full Report (CSV)",
    data=csv_data,
    file_name="pump_health_report.csv",
    mime="text/csv",
)

# --------------------------------------------------------
# OPTIONAL: MAKE REPORT SUMMARY (included in CSV too)
# --------------------------------------------------------
st.subheader("📌 Summary")
total = len(df)
critical = (df["Health Status"] == "🔴 CRITICAL").sum()
warning = (df["Health Status"] == "🟠 WARNING").sum()
normal = (df["Health Status"] == "🟢 NORMAL").sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Rows", total)
col2.metric("Normal", normal)
col3.metric("Warning", warning)
col4.metric("Critical", critical)

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