# --------------------------------------------
# 📦 Project Commands for PDF RAG Chat App
# --------------------------------------------

# ✅ Run the Streamlit app (safe for Mac M1/M2 and Streamlit Cloud)
run:
	KMP_DUPLICATE_LIB_OK=TRUE STREAMLIT_WATCHER_TYPE=none streamlit run main.py

# ✅ Install Python dependencies
install:
	pip install -r requirements.txt

# ✅ Format codebase using Black and isort
fmt:
	black . && isort .

# ✅ Show current LangSmith tracing config
trace:
	@echo "🔍 LangSmith tracing active with project: $${LANGCHAIN_PROJECT:-'not set'}"

# ✅ Create PR: new_pdf_rag_base → dev (prompts for title/body)
pr-dev:
	gh pr create --base dev --head new_pdf_rag_base --web=false

# ✅ Create PR: dev → main (prompts for title/body)
pr-main:
	gh pr create --base main --head dev --web=false
run:
	KMP_DUPLICATE_LIB_OK=TRUE STREAMLIT_WATCHER_TYPE=poll streamlit run main.py