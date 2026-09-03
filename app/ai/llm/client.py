from openai import OpenAI

from app.core.config import settings
from app.ai.llm.exceptions import LLMConfigurationError


class OpenAIClient:
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise LLMConfigurationError(
                "OpenAI API key is not configured."
            )

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )