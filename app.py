import streamlit as st
import traceback

st.title("Startup Diagnostics")

# Step 1
try:
    import config
    st.success("config.py loaded")
except Exception:
    st.error("config.py failed")
    st.text(traceback.format_exc())

# Step 2
try:
    from dialogue.dialogue_manager import DialogueManager
    st.success("dialogue_manager loaded")
except Exception:
    st.error("dialogue_manager failed")
    st.text(traceback.format_exc())

# Step 3
try:
    from nlp.intent_model import predict_intent
    st.success("intent_model loaded")
except Exception:
    st.error("intent_model failed")
    st.text(traceback.format_exc())

# Step 4
try:
    from utils.entity_extractor import extract_entities
    st.success("entity_extractor loaded")
except Exception:
    st.error("entity_extractor failed")
    st.text(traceback.format_exc())

st.success("All imports succeeded")
