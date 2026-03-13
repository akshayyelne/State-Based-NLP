import os
import sqlite3
import pandas as pd
import streamlit as st
import sys

# ======================================
# PATH SETUP
# ======================================
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from dialogue.dialogue_manager import DialogueManager
from config import DB_PATH, BASE_DIR

# ======================================
# CONFIG
# ======================================
from config import ADMIN_PASSWORD


# ======================================
# DATABASE INITIALIZATION
# ======================================
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

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

        # Safe migrations: add any missing columns to existing tables
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

        cursor.execute("""
            INSERT OR IGNORE INTO Policies
            (policy_number, customer_name, dob, vehicle_make, vehicle_year, coverage, premium, status, expiry_date, renewal_date)
            VALUES
            ('P12345','John Smith','01/01/1985','Toyota',2018,'Basic',700,'Active', '23/02/2027', '23/02/2026')
        """)

        cursor.execute("""
            INSERT OR IGNORE INTO Policies
            (policy_number, customer_name, dob, vehicle_make, vehicle_year, coverage, premium, status, expiry_date, renewal_date)
            VALUES
            ('P67890','Alice Brown','10/03/1990','Honda',2020,'Premium',950,'Inactive', '01/01/2025', '01/01/2024')
        """)


# ======================================
# MAIN APPLICATION
# ======================================
def main():

    st.set_page_config(
        page_title="Insurance Assistant",
        layout="wide"
    )

    # Initialize DB once per session
    if "db_initialized" not in st.session_state:
        init_db()
        st.session_state.db_initialized = True

    # Session state setup
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "menu_selection" not in st.session_state:
        st.session_state.menu_selection = "Home"

    menu = ["Home", "Admin Dashboard", "Conversation History", "About"]

    # Sidebar
    if os.path.exists(os.path.join(BASE_DIR, "logo.png")):
        st.sidebar.image(
            os.path.join(BASE_DIR, "logo.png"),
            use_container_width=True
        )

    choice = st.sidebar.selectbox(
        "Menu",
        menu,
        index=menu.index(st.session_state.menu_selection)
    )
    
    if choice != st.session_state.menu_selection:
        if choice == "Home":
            st.session_state.workflow = None
            st.session_state.state = "START"
            st.session_state.chat_history = []
        st.session_state.menu_selection = choice
        st.rerun()

    # Always show "New Conversation" button when on Home
    if choice == "Home":
        st.sidebar.markdown("---")
        if st.sidebar.button("New Conversation", use_container_width=True):
            st.session_state.workflow = None
            st.session_state.state = "START"
            st.session_state.chat_history = []
            st.rerun()

    dm = DialogueManager()

    # ======================================
    # HOME
    # ======================================
    if choice == "Home":

        if os.path.exists(os.path.join(BASE_DIR, "banner.png")):
            st.image(
                os.path.join(BASE_DIR, "banner.png"),
                use_container_width=True
            )

        st.title("Insurance Policy & Claims Assistant")

        chat_container = st.container()

        with chat_container:
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
            except Exception as e:
                response = "An unexpected system error occurred."
                print(e)

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
                st.success("Access granted.")
                st.rerun()
            elif password:
                st.error("Invalid password.")

            st.stop()

        st.title("Admin Dashboard")

        if st.button("Logout"):
            st.session_state.admin_authenticated = False
            st.rerun()

        tab1, tab2 = st.tabs(["Policies", "Claims"])

        with sqlite3.connect(DB_PATH) as conn:

            with tab1:
                st.subheader("All Policies")
                df_policies = pd.read_sql_query("SELECT * FROM Policies", conn)
                st.dataframe(df_policies, use_container_width=True)

                st.download_button(
                    "Download Policies as CSV",
                    df_policies.to_csv(index=False).encode("utf-8"),
                    "policies_report.csv",
                    "text/csv"
                )

            with tab2:
                st.subheader("All Claims")
                df_claims = pd.read_sql_query("SELECT * FROM Claims", conn)

                if not df_claims.empty:
                    status_filter = st.multiselect(
                        "Filter by Status",
                        options=df_claims["status"].unique(),
                        default=df_claims["status"].unique()
                    )

                    df_claims = df_claims[
                        df_claims["status"].isin(status_filter)
                    ]

                st.dataframe(df_claims, use_container_width=True)

                st.download_button(
                    "Download Claims as CSV",
                    df_claims.to_csv(index=False).encode("utf-8"),
                    "claims_report.csv",
                    "text/csv"
                )

    # ======================================
    # CONVERSATION HISTORY
    # ======================================
    elif choice == "Conversation History":

        st.title("Conversation History")

        if not st.session_state.chat_history:
            st.info("No conversation history in this session.")
        else:
            for i, chat in enumerate(st.session_state.chat_history):
                st.write(f"**Round {i+1}**")
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
        that simulates real-world insurance operations through structured, state-driven workflows.

        It combines:
        • Machine Learning intent classification (TF-IDF + Logistic Regression)  
        • Finite State Machine (FSM) dialogue orchestration  
        • Structured underwriting & payment simulation  
        • SQLite-based persistence layer  
        • Secure admin dashboard for monitoring  

        This implementation demonstrates a modular, production-style architecture 
        separating NLP, business logic, workflows, and UI layers.
        """)


# ======================================
# ENTRY POINT
# ======================================
if __name__ == "__main__":
    main()
