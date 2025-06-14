import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def is_streamlit_cloud():
    """
    Detect if the app is running in Streamlit Cloud.
    It checks for known env variables or HOME path containing 'streamlit'.
    """
    return os.getenv("STREAMLIT_ENV", "").lower() == "cloud" or "streamlit" in os.getenv("HOME", "").lower()


def load_and_split_pdf(file_path):
    """
    Loads a PDF file using the best available loader:
    - Tries UnstructuredPDFLoader only if running locally.
    - Always falls back to PyMuPDFLoader (Streamlit-safe).
    - Then splits documents into manageable chunks for LLMs.
    """
    documents = []

    # ✅ Use Unstructured loader only on local (fails on Streamlit due to OpenCV dependency)
    if not is_streamlit_cloud():
        try:
            from langchain_community.document_loaders import UnstructuredPDFLoader
            loader = UnstructuredPDFLoader(file_path)
            documents = loader.load()
            print("✅ Loaded using UnstructuredPDFLoader (local)")
        except Exception as e:
            print(f"⚠️ UnstructuredPDFLoader failed: {e}")
            documents = []

    # ✅ Always fall back to cloud-safe loader
    if not documents:
        print("🔁 Using PyMuPDFLoader (cloud-safe fallback)...")
        loader = PyMuPDFLoader(file_path)
        documents = loader.load()

    # ✅ Split for RAG
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
    chunks = splitter.split_documents(documents)

    return chunks
