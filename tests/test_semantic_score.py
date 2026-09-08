import pytest

from app.ai.embeddings.semantic_score import similarity_to_score


def test_perfect_similarity_returns_100():
    assert similarity_to_score(1.0) == 100.0


def test_zero_similarity_returns_50():
    assert similarity_to_score(0.0) == 50.0


def test_negative_similarity_returns_lower_score():
    assert similarity_to_score(-0.5) == 25.0


def test_minimum_similarity_returns_zero():
    assert similarity_to_score(-1.0) == 0.0


def test_positive_similarity_is_normalized():
    assert similarity_to_score(0.8) == 90.0


def test_similarity_above_range_raises_error():
    with pytest.raises(ValueError, match="between -1.0 and 1.0"):
        similarity_to_score(1.1)


def test_similarity_below_range_raises_error():
    with pytest.raises(ValueError, match="between -1.0 and 1.0"):
        similarity_to_score(-1.1)