import streamlit as st
from login import login_user

st.set_page_config(page_title="Predictive Maintenance System", layout="wide")

# -------------------------------------------------
# Initialize Session State
# -------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None


# -------------------------------------------------
# LOGIN PAGE
# -------------------------------------------------
def login_page():
    st.title("🔐 Predictive Maintenance System")
    st.write("Please log in to continue.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    if col1.button("Log In"):
        role = login_user(username, password)

        if role:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

    st.info("Only Admin can register new users. Ask the admin to create an account for you.")


# -------------------------------------------------
# MAIN APPLICATION (Protected Area)
# -------------------------------------------------
if not st.session_state.logged_in:

    # Sidebar is HIDDEN before login
    st.sidebar.empty()
    login_page()

else:

    # ✅ Sidebar only visible AFTER login
    st.sidebar.success(f"Logged in as: {st.session_state.role}")

    # ADMIN BUTTON (Only for admin)
    if st.session_state.role == "admin":
        if st.sidebar.button("Register New User"):
            st.switch_page("pages/0_Register_User.py")

    # LOGOUT BUTTON
    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.rerun()

    # Main Home Page
    st.title("🏭 Predictive Maintenance System (Oil & Gas)")
    st.write("Use the sidebar to navigate through system modules.")
