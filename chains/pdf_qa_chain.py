from langchain_community.vectorstores import FAISS, Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langsmith import traceable

@traceable(name="PDF QA Chain")
def build_pdf_qa_chain(chunks):
    print(f"✅ Raw chunks received: {len(chunks)}")

    if not chunks or all(c.page_content.strip() == "" for c in chunks):
        for i, c in enumerate(chunks):
            print(f"Chunk {i+1} content preview: {repr(c.page_content[:100])}")
        raise ValueError("❌ No valid content chunks found after splitting. Cannot build FAISS index.")

    embeddings = OpenAIEmbeddings()
    # vectorstore = Chroma.from_documents(chunks, embedding=embeddings, persist_directory="chroma_store")
    # retriever = vectorstore.as_retriever(search_kwargs={"k": 2}) if wanted to use chromadb.
    vectorstore = FAISS.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    # # ✅ Use "question" not "query"
    # prompt = PromptTemplate(
    #     input_variables=["question", "context"],
    #     template="""
    # You are an Amazon interview coach. Use ONLY the following context to give a **detailed, structured, and interview-ready** answer to the question.
    #
    # ### CONTEXT:
    # {context}
    #
    # ### QUESTION:
    # {question}
    #
    # ### FORMAT:
    # - Start with a 1-line summary.
    # - Provide a detailed explanation with examples.
    # - Break down the principle into behavior patterns or sub-points.
    # - If the principle has an Amazon-specific interpretation, include that.
    # - If there's not enough data in context, say: "Not enough information."
    #
    # ### DETAILED ANSWER:
    # """
    # )
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
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )

    return qa_chain