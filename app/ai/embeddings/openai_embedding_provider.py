from openai import OpenAI

from app.ai.embeddings.embedding_provider import EmbeddingProvider
from app.core.config import settings


class OpenAIEmbeddingProvider(EmbeddingProvider):
    MODEL = "text-embedding-3-small"

    def __init__(self) -> None:
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured.")

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
        )

    def embed(self, text: str) -> list[float]:
        cleaned_text = text.strip()

        if not cleaned_text:
            raise ValueError("Text cannot be empty.")

        response = self.client.embeddings.create(
            model=self.MODEL,
            input=cleaned_text,
            encoding_format="float",
        )

        if not response.data:
            raise ValueError("No embedding data returned by OpenAI.")

        return response.data[0].embedding