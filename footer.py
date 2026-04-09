import streamlit as st

def show_footer():
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; font-size: 13px; opacity: 0.7;'>"
        "© 2026 Najmi Dagna Garneta • Predictive Maintenance System"
        "</div>",
        unsafe_allow_html=True
    )