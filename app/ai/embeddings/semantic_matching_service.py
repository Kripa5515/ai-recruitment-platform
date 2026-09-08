from app.ai.embeddings.embedding_service import EmbeddingService
from app.ai.embeddings.semantic_score import similarity_to_score
from app.ai.embeddings.similarity import cosine_similarity


class SemanticMatchingService:
    def __init__(
        self,
        embedding_service: EmbeddingService | None = None,
    ) -> None:
        self.embedding_service = (
            embedding_service or EmbeddingService()
        )

    def calculate_similarity(
        self,
        text_a: str,
        text_b: str,
    ) -> float:
        vector_a = self.embedding_service.embed_vector(text_a)
        vector_b = self.embedding_service.embed_vector(text_b)

        return cosine_similarity(vector_a, vector_b)

    def calculate_score(
        self,
        text_a: str,
        text_b: str,
    ) -> float:
        similarity = self.calculate_similarity(
            text_a=text_a,
            text_b=text_b,
        )

        return similarity_to_score(similarity)

    def match(
        self,
        text_a: str,
        text_b: str,
    ) -> tuple[float, float]:
        similarity = self.calculate_similarity(
            text_a=text_a,
            text_b=text_b,
        )

        score = similarity_to_score(similarity)

        return similarity, score