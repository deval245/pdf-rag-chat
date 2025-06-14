from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import streamlit as st

def is_streamlit_cloud():
    """
    Detects if the code is running on Streamlit Cloud.
    STREAMLIT_ENV or HOME path containing 'streamlit' is a good signal.
    """
    return os.getenv("STREAMLIT_ENV", "").lower() == "cloud" or "streamlit" in os.getenv("HOME", "").lower()

def load_and_split_pdf(file_path):
    documents = []

    # Use Streamlit secret to enable Unstructured
    use_unstructured = st.secrets.get("USE_UNSTRUCTURED", "false").lower() == "true"

    # Try UnstructuredPDFLoader only if enabled and not on Streamlit Cloud
    if use_unstructured and not is_streamlit_cloud():
        try:
            from langchain_community.document_loaders import UnstructuredPDFLoader
            loader = UnstructuredPDFLoader(file_path)
            documents = loader.load()
            print("✅ Loaded with UnstructuredPDFLoader (local)")
        except Exception as e:
            print(f"⚠️ UnstructuredPDFLoader failed: {e}")
            documents = []

    # Fallback: Always safe
    if not documents:
        print("🔁 Using PyMuPDFLoader (Cloud-safe fallback)...")
        loader = PyMuPDFLoader(file_path)
        documents = loader.load()

    # Chunk the documents
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
    chunks = splitter.split_documents(documents)

    return chunks
