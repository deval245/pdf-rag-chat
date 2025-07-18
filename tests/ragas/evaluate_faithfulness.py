# def test_ragas_faithfulness_score():
#     # Placeholder example for RAGAS style test
#     actual_score = 0.95  # Pretend calculated faithfulness score
#     assert actual_score >= 0.8

import pytest
from ragas.metrics import faithfulness
from ragas.evaluation import evaluate

@pytest.mark.ragas
def test_faithfulness_score(rag_test_dataset):
    result = evaluate(rag_test_dataset, metrics=[faithfulness])
    score = result["faithfulness"].score
    assert score >= 0.8, f"Faithfulness score too low: {score}"