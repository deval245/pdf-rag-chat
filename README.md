# # 📄 Chat with Your PDF (LangChain + LangSmith)

Chat with any PDF file using a LangChain-powered RAG pipeline with full tracing via LangSmith.

---

## 🚀 Features

- 📤 Upload any PDF (policy, resume, contract, article, etc.)
- 🤖 Ask natural language questions about its content
- 🔍 Retrieves only relevant chunks using FAISS
- 🔗 Structured LLM response using LangChain
- 📊 Full observability via LangSmith
- 💡 Document-agnostic and prompt-safe

---

## 🧠 Tech Stack

- Python, Streamlit, FastAPI (optional)
- LangChain, FAISS, LangSmith
- OpenAI LLM (or plug your own)
- Unstructured PDF parsing
- Redis/Kafka ready (for future scalability)

---

## 📁 Project Structure

```bash
pdf-rag-chat/
├── chains/               # LangChain logic (RAG)
│   └── pdf_qa_chain.py
├── utils/                # PDF parsing
│   └── pdf_loader.py
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
pip3 install -r requirements.txt

make install

4. Setup your .env file
env

OPENAI_API_KEY=sk-xxx
LANGCHAIN_API_KEY=ls-xxx
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=pdf-rag-chat
🧪 Run the App

make run

or

KMP_DUPLICATE_LIB_OK=TRUE STREAMLIT_WATCHER_TYPE=none streamlit run main.py


📌 LangSmith Tracing
View detailed RAG traces at https://smith.langchain.com

💡 Future Add-ons (PRs Welcome!)
Export answer + source chunks as .txt/.json

Add LangGraph routing for multiple document types

Deploy to Streamlit Cloud with custom subdomain




## 🧠 Architecture: Document-Agnostic LLM RAG Pipeline

/Users/devalthakkar/pdf-rag-chat/img.png

This project follows a modular Retrieval-Augmented Generation (RAG) architecture, built for real-time question answering over any PDF (policy, resume, legal, etc.).

### 🧰 Core Components

| Layer              | Description |
|-------------------|-------------|
| 📄 PDF Loader      | Parses document using `UnstructuredPDFLoader` |
| 🧩 Chunk Splitter  | Splits into context chunks (RecursiveCharacterTextSplitter) |
| 🧠 Embedding Model | OpenAI Embeddings generate semantic vectors |
| 📦 Vector DB       | FAISS (in-memory) or **ChromaDB (persistent)** stores chunks |
| 🔎 Retriever       | Top-k search from VectorDB |
| 💬 LLM             | GPT-3.5-turbo generates structured answers |
| 🔗 Prompt Template | Controlled, context-only prompt with format rules |
| 🔭 LangSmith Trace | Full traceability of chunk retrieval, LLM steps, and responses |
| 🖥️ Streamlit UI    | Simple frontend to upload and chat with PDFs |

---

### 🔁 End-to-End Flow: LLMOps RAG Pipeline

1. **User uploads PDF** → stored locally under `/data`
2. **Chunks created** using tokenizer-aware splitting
3. **Embeddings generated** for chunks via OpenAI
4. **Chunks indexed** into FAISS or Chroma vector DB
5. **User enters question**
6. **Retriever pulls relevant context** from the DB
7. **LLM invoked** with prompt + context → structured answer
8. **Sources + answer shown in UI**
9. **LangSmith logs the entire run** for debugging and observability

🧑‍💻 Author
Deval Thakkar – Sr. Software Engineer | LLM Infra | GenAI Test Architect
📎 LinkedIn

📜 License
MIT License — use freely and contribute!


