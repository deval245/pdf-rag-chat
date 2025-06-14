from utils.env_loader import load_environment, safe_get_env
load_environment()

import os
import streamlit as st
from utils.pdf_loader import load_and_split_pdf
from chains.pdf_qa_chain import build_pdf_qa_chain

# Streamlit config
st.set_page_config(page_title="Chat with Your PDF", layout="centered")
st.title("📄 Chat with Your PDF (LangChain + LangSmith)")

# Backend toggle
backend = st.selectbox("🧠 Choose backend:", ["OpenAI", "Ollama"])

# Upload PDF
uploaded_file = st.file_uploader("📤 Upload a PDF file", type=["pdf"])
if uploaded_file:
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success("✅ PDF uploaded and saved!")

    with st.spinner("⏳ Processing and indexing PDF..."):
        chunks = load_and_split_pdf(file_path)
        st.write(f"✅ {len(chunks)} chunks after splitting and filtering")
        qa_chain = build_pdf_qa_chain(chunks, backend=backend)

    question = st.text_input("❓ Ask a question from the PDF:")
    if question:
        with st.spinner("🧠 Thinking..."):
            result = qa_chain.invoke({"query": question})
            st.markdown(f"### ✅ **Answer:**\n{result['result']}")
            st.markdown("### 📚 Source Chunks:")
            for i, doc in enumerate(result['source_documents']):
                st.markdown(f"**Source {i+1}:**")
                st.code(doc.page_content[:300] + "...")
