import pytest

from app.ai.embeddings.similarity import cosine_similarity


def test_identical_vectors_have_similarity_one():
    vector = [1.0, 2.0, 3.0]

    result = cosine_similarity(vector, vector)

    assert result == pytest.approx(1.0)


def test_orthogonal_vectors_have_similarity_zero():
    vector_a = [1.0, 0.0]
    vector_b = [0.0, 1.0]

    result = cosine_similarity(vector_a, vector_b)

    assert result == pytest.approx(0.0)


def test_opposite_vectors_have_similarity_negative_one():
    vector_a = [1.0, 0.0]
    vector_b = [-1.0, 0.0]

    result = cosine_similarity(vector_a, vector_b)

    assert result == pytest.approx(-1.0)


def test_different_dimensions_raise_error():
    vector_a = [1.0, 2.0]
    vector_b = [1.0, 2.0, 3.0]

    with pytest.raises(ValueError, match="same dimensions"):
        cosine_similarity(vector_a, vector_b)


def test_empty_vector_raises_error():
    with pytest.raises(ValueError, match="cannot be empty"):
        cosine_similarity([], [1.0, 2.0])


def test_zero_vector_raises_error():
    vector_a = [0.0, 0.0]
    vector_b = [1.0, 2.0]

    with pytest.raises(ValueError, match="Zero-vector"):
        cosine_similarity(vector_a, vector_b)


def test_similarity_is_clamped_to_valid_range():
    result = cosine_similarity(
        [1.0, 2.0],
        [1.0, 2.0],
    )

    assert -1.0 <= result <= 1.0