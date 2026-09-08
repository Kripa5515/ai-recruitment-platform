from pydantic import BaseModel, Field


class EmbeddingResult(BaseModel):
    text: str
    vector: list[float] = Field(default_factory=list)
    model: str