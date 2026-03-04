
import streamlit as st
from login import load_users, save_users

# -------------------------------------------------
# ADMIN-ONLY ACCESS CONTROL
# -------------------------------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("❌ Access denied. Please log in first.")
    st.stop()
if st.session_state.role != "admin":
    st.error("❌ Access restricted. Admin only.")
    st.stop()
    
st.title("📝 Register New User")

username = st.text_input("Choose a Username")
password = st.text_input("Choose a Password", type="password")

if st.button("Register"):
    if username.strip() == "" or password.strip() == "":
        st.error("Username and password cannot be empty.")
    else:
        users = load_users()

        if username in users:
            st.error("❌ Username already exists. Choose another.")
        else:
            users[username] = password
            save_users(users)
            st.success("✅ User registered successfully!")
            st.info("You can now login using this new account.")
