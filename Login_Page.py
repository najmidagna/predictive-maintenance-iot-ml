import streamlit as st
from login import login_user
from footer import show_footer



st.set_page_config(page_title="Predictive Maintenance System", layout="wide")

# Session init
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "username" not in st.session_state:
    st.session_state.username = None


# -----------------------------
# LOGIN PAGE
# -----------------------------
def login_page():
    st.title("🔐 Predictive Maintenance System")
    st.write("Please log in to continue.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        role = login_user(username, password)
        if role:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.session_state.username = username
            st.switch_page("pages/0_🏠_Home.py")
        else:
            st.error("❌ Invalid username or password")


# -----------------------------
# MAIN ROUTER
# -----------------------------
if not st.session_state.logged_in:
    login_page()
else:
    st.switch_page("pages/0_🏠_Home.py")

show_footer()