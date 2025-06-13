from langchain_community.document_loaders import UnstructuredPDFLoader, PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_and_split_pdf(file_path):
    # Primary: Try Unstructured
    try:
        loader = UnstructuredPDFLoader(file_path)
        documents = loader.load()
    except Exception as e:
        print(f"⚠️ Unstructured failed: {e}")
        documents = []

    # Fallback if Unstructured fails or returns nothing
    if not documents:
        print("🔁 Falling back to PyMuPDFLoader...")
        loader = PyMuPDFLoader(file_path)
        documents = loader.load()

    # Final chunking
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
    chunks = splitter.split_documents(documents)

    return chunks
