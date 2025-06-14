run:
	KMP_DUPLICATE_LIB_OK=TRUE STREAMLIT_WATCHER_TYPE=poll streamlit run main.py

install:
	pip install -r requirements.txt

fmt:
	black . && isort .

trace:
	echo "LangSmith tracing enabled"

pr-dev:
	gh pr create --base dev --head new_pdf_rag_base --title "$(TITLE)" --body "$(BODY)"

pr-main:
	gh pr create --base main --head dev --title "$(TITLE)" --body "$(BODY)"
