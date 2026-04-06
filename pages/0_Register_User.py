import streamlit as st
from login import load_users, save_users

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
