from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import streamlit as st
import os

def is_streamlit_cloud():
    return os.getenv("STREAMLIT_ENV", "").lower() == "cloud" or "streamlit" in os.getenv("HOME", "").lower()

def safe_get_secret(key, default=None):
    try:
        return st.secrets.get(key, default)
    except Exception:
        return default

def load_and_split_pdf(file_path):
    documents = []

    # Prefer Unstructured if explicitly enabled
    use_unstructured = safe_get_secret("USE_UNSTRUCTURED", "false").lower() == "true"

    if use_unstructured and not is_streamlit_cloud():
        try:
            from langchain_community.document_loaders import UnstructuredPDFLoader
            loader = UnstructuredPDFLoader(file_path)
            documents = loader.load()
            print("✅ Loaded with UnstructuredPDFLoader")
        except Exception as e:
            print(f"⚠️ UnstructuredPDFLoader failed: {e}")
            documents = []

    if not documents:
        print("🔁 Using PyMuPDFLoader (safe fallback)...")
        loader = PyMuPDFLoader(file_path)
        documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
    chunks = splitter.split_documents(documents)

    return chunks
