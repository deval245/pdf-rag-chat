import os
from langchain_community.document_loaders import (
    PyMuPDFLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredPowerPointLoader,
    TextLoader,
    UnstructuredImageLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter

def is_streamlit_cloud():
    return (
        os.getenv("STREAMLIT_ENV", "").lower() == "cloud"
        or "streamlit" in os.getenv("HOME", "").lower()
    )

def load_and_split_any_file(file_path):
    extension = file_path.split(".")[-1].lower()
    documents = []

    try:
        if extension == "pdf":
            print("🔁 Using PyMuPDFLoader for PDF...")
            documents = PyMuPDFLoader(file_path).load()

        elif extension == "docx":
            print("📄 Loading DOCX with UnstructuredWordDocumentLoader...")
            documents = UnstructuredWordDocumentLoader(file_path).load()

        elif extension == "pptx":
            print("📊 Loading PPTX with UnstructuredPowerPointLoader...")
            documents = UnstructuredPowerPointLoader(file_path).load()

        elif extension == "txt":
            print("📝 Loading TXT with TextLoader...")
            documents = TextLoader(file_path).load()

        elif extension in ["png", "jpg", "jpeg"]:
            print("🖼️ Loading image with OCR via UnstructuredImageLoader...")
            documents = UnstructuredImageLoader(file_path).load()

        else:
            raise ValueError(f"❌ Unsupported file type: .{extension}")

    except Exception as e:
        print(f"⚠️ Document load failed: {e}")
        raise

    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
    chunks = splitter.split_documents(documents)
    return chunks
