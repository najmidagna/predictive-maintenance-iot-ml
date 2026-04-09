import streamlit as st
from login import load_users, save_users
from footer import show_footer

# -------------------------------
# ADMIN ACCESS CHECK
# -------------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("❌ Please log in first.")
    st.stop()

if st.session_state.role != "admin":
    st.error("❌ Access denied. Only admin can register new users.")
    st.stop()

# -------------------------------
# UI
# -------------------------------
st.title("📝 Register New User")

username = st.text_input("Choose a Username")
password = st.text_input("Choose a Password", type="password")

if st.button("Register User"):
    users = load_users()

    if username in users:
        st.error("❌ User already exists.")
    else:
        # ⭐ FIXED: Save in correct dictionary format
        users[username] = {
            "password": password,
            "role": "user"
        }
        save_users(users)

        st.success(f"✅ User '{username}' registered successfully!")
        st.info("You can now log in with this new account.")

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