from langchain_community.vectorstores import FAISS, Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langsmith import traceable

@traceable(name="PDF QA Chain")
def build_pdf_qa_chain(chunks, backend="OpenAI"):
    print(f"✅ Raw chunks received: {len(chunks)}")

    if not chunks or all(c.page_content.strip() == "" for c in chunks):
        for i, c in enumerate(chunks):
            print(f"Chunk {i+1} content preview: {repr(c.page_content[:100])}")
        raise ValueError("❌ No valid content chunks found after splitting. Cannot build vector index.")

    # 🔁 Embedding + LLM backend toggle
    if backend == "OpenAI":
        embeddings = OpenAIEmbeddings()
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    else:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        llm = Ollama(model="mistral")

    # 🧠 Use FAISS for in-memory or switch to Chroma (optional)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    # 🔮 Smart prompt for dynamic domain answers
    prompt = PromptTemplate(
        input_variables=["question", "context"],
        template="""
    You are a domain-agnostic expert assistant. Use ONLY the following context to generate a detailed, structured, and task-appropriate answer to the question provided.

    ### CONTEXT:
    {context}

    ### QUESTION:
    {question}

    ### FORMAT:
    - Begin with a 1-line summary of the answer.
    - Provide a detailed explanation, using examples if possible.
    - Break down the information into clear, logical sub-points or bullet points.
    - Tailor your tone and terminology to match the document's domain (e.g., policy, education, sports, legal).
    - If the context does not contain enough information, respond exactly with: "Not enough information."

    ### ANSWER:
    """
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )

    return qa_chain
