from app.ai.embeddings.embedding_provider import EmbeddingProvider
from app.ai.embeddings.embedding_service import EmbeddingService


class FakeEmbeddingProvider(EmbeddingProvider):
    MODEL = "fake-embedding-model"

    def embed(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]


def test_embedding_service_returns_embedding_result():
    service = EmbeddingService(
        provider=FakeEmbeddingProvider(),
    )

    result = service.embed("Python developer with FastAPI experience")

    assert result.text == "Python developer with FastAPI experience"
    assert result.vector == [0.1, 0.2, 0.3]
    assert result.model == "fake-embedding-model"


def test_embedding_service_returns_vector():
    service = EmbeddingService(
        provider=FakeEmbeddingProvider(),
    )

    vector = service.embed_vector(
        "Python developer with FastAPI experience",
    )

    assert vector == [0.1, 0.2, 0.3]


def test_embedding_provider_receives_text():
    class TrackingProvider(EmbeddingProvider):
        MODEL = "tracking-model"

        def __init__(self):
            self.received_text = None

        def embed(self, text: str) -> list[float]:
            self.received_text = text
            return [1.0, 2.0]

    provider = TrackingProvider()

    service = EmbeddingService(provider=provider)

    service.embed("AI Engineer")

    assert provider.received_text == "AI Engineer"