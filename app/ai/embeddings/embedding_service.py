from app.ai.embeddings.embedding_provider import EmbeddingProvider
from app.ai.embeddings.openai_embedding_provider import (
    OpenAIEmbeddingProvider,
)
from app.ai.embeddings.schemas import EmbeddingResult


class EmbeddingService:
    def __init__(
        self,
        provider: EmbeddingProvider | None = None,
    ) -> None:
        self.provider = provider or OpenAIEmbeddingProvider()

    def embed(self, text: str) -> EmbeddingResult:
        vector = self.provider.embed(text)

        return EmbeddingResult(
            text=text,
            vector=vector,
            model=self._get_model_name(),
        )

    def embed_vector(self, text: str) -> list[float]:
        return self.provider.embed(text)

    def _get_model_name(self) -> str:
        model = getattr(self.provider, "MODEL", None)

        if model:
            return model

        return self.provider.__class__.__name__