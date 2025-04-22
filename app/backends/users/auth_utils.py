import streamlit as st
from app.backends.users.models import verify_user

def authenticate_user():
    """Streamlit-based authentication."""
    st.title("🔐 Xtrium Login")

    email = st.text_input("Email", key="email_input")
    password = st.text_input("Password", type="password", key="password_input")

    if st.button("Login"):
        if verify_user(email, password):
            st.session_state["authenticated"] = True
            st.session_state["user_email"] = email
            st.success("✅ Login successful!")
            return True
        else:
            st.error("❌ Invalid email or password")
    
    return False