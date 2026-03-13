import streamlit as st
import traceback

try:
    import os
    import sqlite3
    import pandas as pd
    import sys

    # PATH SETUP
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)

    from dialogue.dialogue_manager import DialogueManager
    from config import DB_PATH, BASE_DIR, ADMIN_PASSWORD

except Exception:
    st.title("Startup Error")
    st.text(traceback.format_exc())
    st.stop()


# ======================================
# CACHE HEAVY OBJECTS
# ======================================

@st.cache_resource
def get_dialogue_manager():
    return DialogueManager()
    
# ======================================

# DATABASE INITIALIZATION

# ======================================

def init_db():
with sqlite3.connect(DB_PATH) as conn:
cursor = conn.cursor()

```
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Policies (
            policy_number TEXT PRIMARY KEY,
            customer_name TEXT,
            dob TEXT,
            vehicle_make TEXT,
            vehicle_year INTEGER,
            coverage TEXT,
            premium REAL,
            status TEXT,
            expiry_date TEXT,
            renewal_date TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Claims (
            claim_id TEXT PRIMARY KEY,
            policy_number TEXT,
            date TEXT,
            type TEXT,
            description TEXT,
            status TEXT,
            amount REAL,
            assigned_officer TEXT,
            risk_flag TEXT,
            last_updated TEXT
        )
    """)

    # Safe schema migration
    claims_cols = [r[1] for r in cursor.execute("PRAGMA table_info(Claims)").fetchall()]
    for col, col_type in [
        ("amount", "REAL"),
        ("assigned_officer", "TEXT"),
        ("risk_flag", "TEXT"),
        ("last_updated", "TEXT")
    ]:
        if col not in claims_cols:
            cursor.execute(f"ALTER TABLE Claims ADD COLUMN {col} {col_type}")

    policy_cols = [r[1] for r in cursor.execute("PRAGMA table_info(Policies)").fetchall()]
    for col, col_type in [
        ("expiry_date", "TEXT"),
        ("renewal_date", "TEXT")
    ]:
        if col not in policy_cols:
            cursor.execute(f"ALTER TABLE Policies ADD COLUMN {col} {col_type}")

    # Seed data
    cursor.execute("""
        INSERT OR IGNORE INTO Policies
        VALUES ('P12345','John Smith','01/01/1985','Toyota',2018,'Basic',700,'Active','23/02/2027','23/02/2026')
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO Policies
        VALUES ('P67890','Alice Brown','10/03/1990','Honda',2020,'Premium',950,'Inactive','01/01/2025','01/01/2024')
    """)
```

# ======================================

# MAIN APPLICATION

# ======================================

def main():

```
st.set_page_config(
    page_title="Insurance Assistant",
    layout="wide"
)

# Initialize database once
if "db_initialized" not in st.session_state:
    init_db()
    st.session_state.db_initialized = True

# Session states
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "menu_selection" not in st.session_state:
    st.session_state.menu_selection = "Home"

menu = ["Home", "Admin Dashboard", "Conversation History", "About"]

# Sidebar branding
logo_path = os.path.join(BASE_DIR, "logo.png")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)

choice = st.sidebar.selectbox(
    "Menu",
    menu,
    index=menu.index(st.session_state.menu_selection)
)

# Reset chat when switching back to Home
if choice != st.session_state.menu_selection:
    if choice == "Home":
        st.session_state.workflow = None
        st.session_state.state = "START"
        st.session_state.chat_history = []
    st.session_state.menu_selection = choice
    st.rerun()

# New conversation button
if choice == "Home":
    st.sidebar.markdown("---")
    if st.sidebar.button("New Conversation", use_container_width=True):
        st.session_state.workflow = None
        st.session_state.state = "START"
        st.session_state.chat_history = []
        st.rerun()

dm = get_dialogue_manager()

# ======================================
# HOME CHAT
# ======================================
if choice == "Home":

    banner_path = os.path.join(BASE_DIR, "banner.png")
    if os.path.exists(banner_path):
        st.image(banner_path, use_container_width=True)

    st.title("Insurance Policy & Claims Assistant")

    for chat in st.session_state.chat_history:
        st.write(f"You: {chat['user']}")
        st.write(f"Bot: {chat['bot']}")
        st.markdown("---")

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("You:")
        submitted = st.form_submit_button("Send")

    if submitted and user_input:
        try:
            response = dm.handle(user_input)
        except Exception:
            response = "System error occurred."
            st.text(traceback.format_exc())

        st.session_state.chat_history.append({
            "user": user_input,
            "bot": response
        })

        st.rerun()

# ======================================
# ADMIN DASHBOARD
# ======================================
elif choice == "Admin Dashboard":

    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False

    if not st.session_state.admin_authenticated:

        st.title("Admin Login")

        password = st.text_input(
            "Enter Admin Password",
            type="password"
        )

        if password == ADMIN_PASSWORD:
            st.session_state.admin_authenticated = True
            st.success("Access granted")
            st.rerun()

        elif password:
            st.error("Invalid password")

        st.stop()

    st.title("Admin Dashboard")

    if st.button("Logout"):
        st.session_state.admin_authenticated = False
        st.rerun()

    tab1, tab2 = st.tabs(["Policies", "Claims"])

    with sqlite3.connect(DB_PATH) as conn:

        with tab1:
            df_policies = pd.read_sql_query("SELECT * FROM Policies", conn)
            st.dataframe(df_policies, use_container_width=True)

        with tab2:
            df_claims = pd.read_sql_query("SELECT * FROM Claims", conn)
            st.dataframe(df_claims, use_container_width=True)

# ======================================
# HISTORY
# ======================================
elif choice == "Conversation History":

    st.title("Conversation History")

    if not st.session_state.chat_history:
        st.info("No conversation history available.")
    else:
        for i, chat in enumerate(st.session_state.chat_history):
            st.write(f"Round {i+1}")
            st.write(f"User: {chat['user']}")
            st.write(f"Bot: {chat['bot']}")
            st.markdown("---")

# ======================================
# ABOUT
# ======================================
elif choice == "About":

    st.title("About")

    st.write("""
    The Insurance Policy & Claims Assistant is an NLP-powered conversational system
    that simulates real-world insurance operations through structured workflows.

    Architecture:
    • Intent classification (TF-IDF + Logistic Regression)
    • Finite State Machine dialogue manager
    • SQLite persistence
    • Admin dashboard
    """)
```

# ======================================
# SAFE APP EXECUTION
# ======================================

def run_app():
    main()

try:
    run_app()
except Exception:
    st.title("Application Error")
    st.text(traceback.format_exc())

