from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def is_streamlit_cloud():
    """
    Detects if the code is running on Streamlit Cloud.
    STREAMLIT_ENV or HOME path containing 'streamlit' is a good signal.
    """
    return os.getenv("STREAMLIT_ENV", "").lower() == "cloud" or "streamlit" in os.getenv("HOME", "").lower()

def load_and_split_pdf(file_path):
    documents = []

    # Try UnstructuredPDFLoader only if running locally
    if not is_streamlit_cloud():
        try:
            from langchain_community.document_loaders import UnstructuredPDFLoader
            loader = UnstructuredPDFLoader(file_path)
            documents = loader.load()
            print("✅ Loaded with UnstructuredPDFLoader (local)")
        except Exception as e:
            print(f"⚠️ UnstructuredPDFLoader failed: {e}")
            documents = []

    # Fallback: Always safe on Streamlit or if Unstructured fails
    if not documents:
        print("🔁 Using PyMuPDFLoader (Cloud-safe fallback)...")
        loader = PyMuPDFLoader(file_path)
        documents = loader.load()

    # Split documents into chunks for LLM processing
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
    chunks = splitter.split_documents(documents)

    return chunks
