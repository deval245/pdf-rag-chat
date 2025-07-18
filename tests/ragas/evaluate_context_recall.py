# def test_ragas_context_recall_score():
#     actual_score = 0.92
#     assert actual_score >= 0.8

import pytest
from ragas.metrics import context_recall
from ragas.evaluation import evaluate

@pytest.mark.ragas
def test_context_recall_score(rag_test_dataset):
    result = evaluate(rag_test_dataset, metrics=[context_recall])
    score = result["context_recall"].score
    assert score >= 0.7, f"Context recall score too low: {score}"