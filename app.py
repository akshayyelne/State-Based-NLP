import streamlit as st
import traceback

st.title("Debug Startup")

try:
    import os
    import sys
    import sqlite3
    import pandas as pd

    st.write("Basic imports successful")

    from dialogue.dialogue_manager import DialogueManager
    st.write("DialogueManager imported")

    dm = DialogueManager()
    st.write("DialogueManager initialized")

    st.success("Application loaded successfully")

except Exception:
    st.error("Application crashed")
    st.text(traceback.format_exc())
