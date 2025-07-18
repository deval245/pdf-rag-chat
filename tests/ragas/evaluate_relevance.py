# def test_ragas_relevance_score():
#     actual_score = 0.9
#     assert actual_score >= 0.8

import pytest
from ragas.metrics import answer_relevancy
from ragas.evaluation import evaluate

@pytest.mark.ragas
def test_relevance_score(rag_test_dataset):
    result = evaluate(rag_test_dataset, metrics=[answer_relevancy])
    score = result["answer_relevancy"].score
    assert score >= 0.7, f"Relevance score too low: {score}"