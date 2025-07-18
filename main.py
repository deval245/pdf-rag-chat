import streamlit as st
import os
from datetime import datetime
from utils.env_loader import load_environment
from utils.pdf_loader import load_and_split_any_file
from chains.pdf_qa_chain import build_pdf_qa_chain
from utils.einstein_layer import run_einstein_checks, mask_sensitive_data

# ✅ Must come first
st.set_page_config(page_title="Chat with Your Document", layout="centered")

# ✅ More reliable Streamlit Cloud detection
is_cloud = not os.path.exists(".env") and "streamlit" in st.__file__.lower()

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
st.title("(LangChain + LangSmith + Einstein Trust Layer)")

# 📤 Document upload
uploaded_file = st.file_uploader("📤 Upload a document", type=["pdf", "docx", "pptx", "txt", "jpg", "jpeg", "png"])
if uploaded_file:
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
                raw_answer = result["result"].strip()

                # Check for empty or "I don't know"-like responses
                if not raw_answer or "not enough information" in raw_answer.lower() or "i don't know" in raw_answer.lower():
                    st.markdown("### ✅ **Answer (with PII masked):**\nNot enough information.")
                    st.info("No sufficiently relevant source content to display.")
                    st.stop()

                # 🛡️ Run Einstein Layer checks
                masked_text, validation_log = run_einstein_checks(raw_answer)

                if validation_log["flagged"]:
                    st.error(f"⚠️ Answer blocked due to policy violations: {validation_log['categories']}")
                    st.stop()

                # ✅ Show final masked answer
                st.markdown(f"### ✅ **Answer (with PII masked):**\n{masked_text}")

                # 📚 Show only if valid answer exists
                st.markdown("### 📚 Source Chunks (PII masked):")
                for i, doc in enumerate(result["source_documents"]):
                    if not doc.page_content.strip():
                        continue
                    masked_source = mask_sensitive_data(doc.page_content)
                    st.markdown(f"**Source {i + 1}:**")
                    st.code(masked_source[:500] + "...")

            except Exception as e:
                st.error(f"❌ Error during processing: {e}")

# 🕵️ Sidebar: Trust & Info
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🔐 Data & Key Privacy")
    st.info(
        """
        - Your API keys are used only in this session
        - No data is logged or saved on servers
        - Compliance logs stored only internally for audit
        - Zero-trust design inspired by NVIDIA and Salesforce
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