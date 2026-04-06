import streamlit as st
import pandas as pd

# --------------------------------------------------------
# ACCESS PROTECTION
# --------------------------------------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("❌ Please log in first.")
    st.stop()

st.title("📘 Detailed Equipment Log")

# --------------------------------------------------------
# CHECK IF ANY LOGS EXIST
# --------------------------------------------------------
if "logs" not in st.session_state or st.session_state.logs is None or st.session_state.logs.empty:
    st.warning("⚠ No equipment logs available. Please run a prediction first.")
    st.stop()

df = st.session_state.logs.copy()

# --------------------------------------------------------
# FILTERING
# --------------------------------------------------------
st.subheader("🔎 Filter Log Entries")

filter_option = st.selectbox(
    "Select Health Status:",
    ["All", "🟢 NORMAL", "🟠 WARNING", "🔴 CRITICAL"]
)

if filter_option == "All":
    df_filtered = df
else:
    df_filtered = df[df["Health Status"] == filter_option]

# --------------------------------------------------------
# SHOW LOG TABLE
# --------------------------------------------------------
st.subheader("📋 Equipment Log Records")
st.dataframe(df_filtered, use_container_width=True)

# --------------------------------------------------------
# SUMMARY PANEL
# --------------------------------------------------------
st.subheader("📊 Summary")

total = len(df)
normal = (df["Health Status"] == "🟢 NORMAL").sum()
warning = (df["Health Status"] == "🟠 WARNING").sum()
critical = (df["Health Status"] == "🔴 CRITICAL").sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Records", total)
col2.metric("Normal", normal)
col3.metric("Warnings", warning)
col4.metric("Critical", critical)

# --------------------------------------------------------
# DOWNLOAD FILTERED CSV
# --------------------------------------------------------
st.subheader("⬇ Download Filtered Log (CSV)")

csv = df_filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="equipment_log.csv",
    mime="text/csv"
)
