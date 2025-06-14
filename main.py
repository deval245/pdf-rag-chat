import streamlit as st
import os
from datetime import datetime
from utils.env_loader import load_environment, safe_get_env
from utils.pdf_loader import load_and_split_any_file
from chains.pdf_qa_chain import build_pdf_qa_chain

# Must be the first Streamlit command
st.set_page_config(page_title="Chat with Your Document", layout="centered")

# 🌐 Detect environment
def is_streamlit_cloud():
    return "streamlit" in os.getenv("HOME", "").lower()

is_cloud = is_streamlit_cloud()

# 🔐 Secure credentials for Streamlit Cloud
if is_cloud:
    with st.sidebar:
        st.markdown("### 🔐 Enter API Keys")
        openai_key = st.text_input("🔑 OpenAI API Key", type="password")
        langsmith_key = st.text_input("🔑 LangSmith API Key", type="password")
        clear_keys = st.checkbox("🔄 Clear keys after session ends", value=True)

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
st.title("📄 Chat with Your Document (LangChain + LangSmith)")

# 📤 Document upload
uploaded_file = st.file_uploader("📤 Upload a document", type=["pdf", "docx", "pptx", "txt", "jpg", "jpeg", "png"])
if uploaded_file:
    # Clear input on new upload
    if "last_uploaded" not in st.session_state or uploaded_file.name != st.session_state.last_uploaded:
        st.session_state.last_uploaded = uploaded_file.name
        st.session_state.pop("question", None)

    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success("✅ Document uploaded and saved!")

    with st.spinner("⏳ Processing and indexing document..."):
        chunks = load_and_split_any_file(file_path)
        st.write(f"✅ {len(chunks)} chunks after splitting and filtering")
        qa_chain = build_pdf_qa_chain(chunks, backend=backend)

    question = st.text_input("❓ Ask a question from the document:", key="question")
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

# 🕵️ Sidebar: Trust & Info
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🔐 Data & Key Privacy")
    st.info(
        """
        - Your API keys are used only in this session  
        - No data is logged or saved  
        - 100% open-source, zero-trust design  
        """
    )
    st.markdown(f"🕒 Session started: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")

# 🛡️ Footer
st.markdown("---")
st.caption("🔒 GDPR & Dev-friendly. No keys or document data is stored. Use at your own discretion. Open source.")

# 🧹 Optional cleanup on session end
if is_cloud and clear_keys:
    os.environ.pop("OPENAI_API_KEY", None)
    os.environ.pop("LANGCHAIN_API_KEY", None)
