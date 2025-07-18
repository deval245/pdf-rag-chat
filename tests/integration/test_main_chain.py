import os
import pytest
from chains.pdf_qa_chain import build_pdf_qa_chain
from utils.env_loader import load_environment
from langchain_core.documents import Document

@pytest.fixture(scope="module", autouse=True)
def load_env_once():
    load_environment()

@pytest.fixture
def sample_chunks():
    return [Document(page_content="Test content about AI and Salesforce.")]

def test_chain_instantiation(sample_chunks):
    chain = build_pdf_qa_chain(sample_chunks, backend="OpenAI")
    assert chain is not None

def test_chain_invoke(sample_chunks):
    chain = build_pdf_qa_chain(sample_chunks, backend="OpenAI")
    query = {"query": "What does it say about Salesforce?"}
    result = chain.invoke(query)
    assert "Salesforce" in result["result"] or result["result"] == "Not enough information."