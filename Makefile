run:
	streamlit run main.py

install:
	pip install -r requirements.txt

fmt:
	black . && isort .

trace:
	echo "LangSmith tracing active"

run:
	KMP_DUPLICATE_LIB_OK=TRUE STREAMLIT_WATCHER_TYPE=none streamlit run main.py