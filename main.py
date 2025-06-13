import os
import streamlit as st
from dotenv import load_dotenv
from utils.pdf_loader import load_and_split_pdf
from chains.pdf_qa_chain import build_pdf_qa_chain

# Load environment variables
load_dotenv()

# Streamlit App Settings
st.set_page_config(page_title="Chat with Your PDF", layout="centered")
st.title("📄 Chat with Your PDF (LangChain + LangSmith)")

# Upload PDF
uploaded_file = st.file_uploader("📤 Upload a PDF file", type=["pdf"])
if uploaded_file:
    file_path = f"data/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success("✅ PDF uploaded and saved!")

    with st.spinner("⏳ Processing and indexing PDF..."):
        chunks = load_and_split_pdf(file_path)
        st.write(f"✅ {len(chunks)} chunks after splitting and filtering")
        qa_chain = build_pdf_qa_chain(chunks)

    # Question input
    query = st.text_input("❓ Ask a question from the PDF:")
    if query:
        with st.spinner("🧠 Thinking..."):
            # DEBUG: Show what's being sent to the LLM
            st.write("🔍 Sending to LLM:", {"query": query})

            # Call the chain (IMPORTANT: match expected input key)
            result = qa_chain.invoke({"query": query})

            # Final Answer
            st.markdown(f"### ✅ **Answer:**\n{result['result']}")

            # Show sources
            st.markdown("### 📚 Source Chunks:")
            for i, doc in enumerate(result['source_documents']):
                st.markdown(f"**Source {i+1}:**")
                st.code(doc.page_content[:300] + "...")

            # Debug: Show full retrieved chunks
            st.markdown("### 🧩 Retrieved Chunks (Debug View):")
            for i, doc in enumerate(result['source_documents']):
                st.markdown(f"**Chunk {i+1}:**")
                st.code(doc.page_content[:500])