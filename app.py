import streamlit as st
import traceback

st.title("Streamlit Startup Debug")

try:
    st.write("Step 1: basic imports")

    import os
    import sys
    import sqlite3
    import pandas as pd

    st.write("Step 2: path setup")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)

    st.write("Step 3: importing config")

    from config import DB_PATH
    st.write(f"DB_PATH = {DB_PATH}")

    st.write("Step 4: importing dialogue manager")

    from dialogue.dialogue_manager import DialogueManager

    st.write("Step 5: creating dialogue manager")

    dm = DialogueManager()

    st.success("App loaded successfully!")

except Exception:
    st.error("Startup failure")
    st.text(traceback.format_exc())
