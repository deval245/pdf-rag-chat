import streamlit as st
st.set_page_config(page_title="Chat with Your PDF", layout="centered")

import os
from utils.env_loader import load_environment, safe_get_env
from utils.pdf_loader import load_and_split_pdf
from chains.pdf_qa_chain import build_pdf_qa_chain

# 🌐 Detect environment
def is_streamlit_cloud():
    return "streamlit" in os.getenv("HOME", "").lower()

is_cloud = is_streamlit_cloud()

# 🔐 Secure credentials for Streamlit Cloud
if is_cloud:
    openai_key = st.text_input("🔑 Enter your OpenAI API key:", type="password")
    langsmith_key = st.text_input("🔑 Enter your LangSmith API key:", type="password")

    if not openai_key or not langsmith_key:
        st.warning("🚨 Please provide both OpenAI and LangSmith API keys to proceed.")
        st.stop()

    os.environ["OPENAI_API_KEY"] = openai_key
    os.environ["LANGCHAIN_API_KEY"] = langsmith_key
else:
    load_environment()

# 🧠 Backend toggle
backend_options = ["OpenAI"]
if not is_cloud:
    backend_options.append("Ollama")
backend = st.selectbox("🧠 Choose backend:", backend_options)

# 🧾 UI
st.title("📄 Chat with Your PDF (LangChain + LangSmith)")

# 📤 PDF upload
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
            try:
                result = qa_chain.invoke({"query": question})
                st.markdown(f"### ✅ **Answer:**\n{result['result']}")
                st.markdown("### 📚 Source Chunks:")
                for i, doc in enumerate(result['source_documents']):
                    st.markdown(f"**Source {i+1}:**")
                    st.code(doc.page_content[:300] + "...")
            except Exception as e:
                st.error(f"❌ Error during processing: {e}")
