from typing import TypeVar

from openai import OpenAI
from pydantic import BaseModel

from app.ai.llm.exceptions import LLMConfigurationError
from app.core.config import settings


T = TypeVar("T", bound=BaseModel)


class OpenAIClient:
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise LLMConfigurationError(
                "OPENAI_API_KEY is not configured."
            )

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def parse(
        self,
        system_prompt: str,
        user_prompt: str,
        response_model: type[T],
        model: str = "gpt-4o-mini",
    ) -> T:

        response = self.client.responses.parse(
            model=model,
            input=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            text_format=response_model,
        )

        return response.output_parsed