class LLMError(Exception):
    """Base exception for LLM-related errors."""


class LLMConfigurationError(LLMError):
    """Raised when LLM configuration is invalid."""


class LLMProviderError(LLMError):
    """Raised when an LLM provider request fails."""