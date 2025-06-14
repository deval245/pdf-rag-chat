📄 Chat with Your PDF (LangChain + LangSmith)

Chat with any PDF file using a LangChain-powered RAG pipeline with full tracing via LangSmith.

🚀 Features

📤 Upload any PDF (policy, resume, contract, article, etc.)

🤖 Ask natural language questions about its content

🔍 Retrieves only relevant chunks using FAISS

🔗 Structured LLM response using LangChain

📊 Full observability via LangSmith

💡 Document-agnostic and prompt-safe


🧠 Tech Stack

Python, Streamlit

LangChain, FAISS, LangSmith

OpenAI LLM (or Ollama for local use)

Unstructured PDF parsing



📁 Project Structure

pdf-rag-chat/
├── chains/               # LangChain logic (RAG)
│   └── pdf_qa_chain.py
├── utils/                # PDF parsing + env loader
│   ├── pdf_loader.py
│   └── env_loader.py
├── data/                 # Uploaded PDFs (auto-cleared, gitignored)
├── .env                  # API Keys (ignored)
├── main.py               # Streamlit app
├── Makefile              # Quick commands
├── requirements.txt      
└── README.md             



⚙️ Setup

1. Clone and enter project

git clone https://github.com/yourname/pdf-rag-chat.git
cd pdf-rag-chat

2. Create virtual environment

python3 -m venv venv
source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt
# or
make install


4. Setup your .env file for local development

OPENAI_API_KEY=sk-...
LANGCHAIN_API_KEY=ls-...
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=pdf-rag-chat

For Streamlit Cloud, keys are entered manually in the UI.




🔐 Bring Your Own Key (BYOK) ** most imp

To run this app:

You need your own OpenAI API Key.

Locally, you can use Ollama to avoid key usage.

On Streamlit Cloud, Ollama is NOT supported (no system-level access).

Add your API keys securely via .env file or .streamlit/secrets.toml.

📦 Tip: This app respects your backend toggle and works seamlessly across environments.




🧪 Run the App

Locally

make run
# or
KMP_DUPLICATE_LIB_OK=TRUE streamlit run main.py

Streamlit Cloud

Push to GitHub and deploy via https://streamlit.io/cloud

Only OpenAI backend is available

Keys prompted from user and not hardcoded



🔐 Secure Credential Handling

In local dev, keys loaded from .env file

In Streamlit Cloud, keys prompted via password field

✅ Keeps your OpenAI and LangSmith keys private



📌 LangSmith Tracing

View full traces and debugging on: https://smith.langchain.com



🧠 Architecture: Document-Agnostic LLM RAG Pipeline

This project follows a modular Retrieval-Augmented Generation (RAG) architecture, built for real-time question answering over any PDF (policy, resume, legal, etc.).



🧰 Core Components

Layer

Description

📄 PDF Loader

Parses document using UnstructuredPDFLoader or PyMuPDFLoader



🧩 Chunk Splitter

Splits into context chunks (RecursiveCharacterTextSplitter)



🧠 Embedding Model

OpenAI or HuggingFace sentence embeddings



📦 Vector DB

FAISS (in-memory) or ChromaDB (extensible)

🔎 Retriever

Top-k search using LangChain retriever


💬 LLM

GPT-3.5-turbo (OpenAI) or Mistral via Ollama


🔗 Prompt Template

Domain-aware and format-specific prompts


🔭 LangSmith Trace

Full observability of RAG pipeline


🖥️ Streamlit UI

Drag-and-drop PDF + chat interface


🔁 End-to-End Flow

User uploads PDF → stored locally in /data

Chunks created with smart overlap for context

Embeddings generated using backend model

Chunks indexed into FAISS

Question entered by user

Top-K context retrieved

LLM invoked with prompt + context

Answer + sources displayed

LangSmith logs the session


🧑‍💻 Author

Deval Thakkar – Sr. Software Engineer | LLM Infra | GenAI Test Architect🔗 https://www.linkedin.com/in/deval-t-a05486299/


📜 License

MIT License — use freely and contribute!

