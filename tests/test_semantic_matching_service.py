from app.ai.embeddings.embedding_provider import EmbeddingProvider
from app.ai.embeddings.embedding_service import EmbeddingService
from app.ai.embeddings.semantic_matching_service import (
    SemanticMatchingService,
)


class FakeEmbeddingProvider(EmbeddingProvider):
    MODEL = "fake-model"

    def embed(self, text: str) -> list[float]:
        if text == "jd":
            return [1.0, 0.0]

        if text == "matching candidate":
            return [1.0, 0.0]

        if text == "different candidate":
            return [0.0, 1.0]

        return [1.0, 0.0]


def create_service() -> SemanticMatchingService:
    embedding_service = EmbeddingService(
        provider=FakeEmbeddingProvider(),
    )

    return SemanticMatchingService(
        embedding_service=embedding_service,
    )


def test_identical_texts_have_high_similarity():
    service = create_service()

    similarity = service.calculate_similarity(
        "jd",
        "matching candidate",
    )

    assert similarity == 1.0


def test_different_texts_have_zero_similarity():
    service = create_service()

    similarity = service.calculate_similarity(
        "jd",
        "different candidate",
    )

    assert similarity == 0.0


def test_calculate_score_returns_100_for_identical_vectors():
    service = create_service()

    score = service.calculate_score(
        "jd",
        "matching candidate",
    )

    assert score == 100.0


def test_calculate_score_returns_50_for_orthogonal_vectors():
    service = create_service()

    score = service.calculate_score(
        "jd",
        "different candidate",
    )

    assert score == 50.0


def test_match_returns_similarity_and_score():
    service = create_service()

    similarity, score = service.match(
        "jd",
        "matching candidate",
    )

    assert similarity == 1.0
    assert score == 100.0