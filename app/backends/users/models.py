import streamlit as st
import sqlite3
import bcrypt
import os

# Get absolute path dynamically
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
DB_PATH = os.path.join(BASE_DIR, "app", "backends", "users", "users.db")
st.write(DB_PATH)

#DB_PATH = "/absolute/path/to/xtrium/database/users.db"

def create_users_table():
    """Create users table if it does not exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_user(email, password):
    """Add a new user (hashed password) to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    try:
        cursor.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", (email, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"User {email} already exists.")
    finally:
        conn.close()

def verify_user(email, password):
    """Verify user credentials."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user and bcrypt.checkpw(password.encode(), user[0].encode()):
        return True
    return False