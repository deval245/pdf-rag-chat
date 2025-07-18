import pytest
from ragas.testset import Testset

@pytest.fixture(scope="session")
def rag_test_dataset():
    return Testset.from_dict({
        "questions": ["What is Deval's tech stack?"],
        "contexts": [["Deval has expertise in Python, FastAPI, LangChain, and AWS."]],
        "answers": ["Python, FastAPI, LangChain, AWS"]
    })