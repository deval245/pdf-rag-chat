from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def is_streamlit_cloud():
    # Streamlit Cloud sets this when deployed
    return os.getenv("STREAMLIT_ENV", "").lower() == "cloud" or "streamlit" in os.getenv("HOME", "").lower()

def load_and_split_pdf(file_path):
    documents = []

    if not is_streamlit_cloud():
        try:
            from langchain_community.document_loaders import UnstructuredPDFLoader
            loader = UnstructuredPDFLoader(file_path)
            documents = loader.load()
            print("✅ Loaded with UnstructuredPDFLoader (local)")
        except Exception as e:
            print(f"⚠️ UnstructuredPDFLoader failed: {e}")
            documents = []

    if not documents:
        print("🔁 Using PyMuPDFLoader (Cloud-safe)...")
        loader = PyMuPDFLoader(file_path)
        documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
    chunks = splitter.split_documents(documents)

    return chunks
