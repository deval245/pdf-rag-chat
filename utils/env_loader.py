import os
from dotenv import load_dotenv
import streamlit as st

def using_streamlit_secrets():
    """Return True if secrets.toml is available in Streamlit Cloud or local .streamlit folder."""
    secrets_path = os.path.join(os.getcwd(), ".streamlit", "secrets.toml")
    return os.environ.get("STREAMLIT_ENV", "").lower() == "cloud" or os.path.exists(secrets_path)

def safe_get_env(key, default=""):
    """Read from st.secrets if in Streamlit cloud or secrets.toml exists, else use .env."""
    if using_streamlit_secrets():
        try:
            return st.secrets.get(key, default)
        except Exception:
            return default
    return os.getenv(key, default)

def load_environment():
    """Load .env in local if not using secrets.toml."""
    if not using_streamlit_secrets():
        load_dotenv()
