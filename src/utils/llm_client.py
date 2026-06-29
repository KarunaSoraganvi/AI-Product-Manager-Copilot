"""LLM client configuration and management."""

import logging
from typing import Optional
from langchain_openai import ChatOpenAI
from anthropic import Anthropic
from config.settings import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """Unified LLM client supporting multiple providers."""

    def __init__(self, provider: str = None, model: str = None):
        """Initialize LLM client."""
        self.provider = provider or settings.LLM_PROVIDER
        self.model = model or settings.DEFAULT_MODEL
        self.client = self._initialize_client()
        logger.info(f"Initialized LLM client: {self.provider}/{self.model}")

    def _initialize_client(self):
        """Initialize appropriate LLM client based on provider."""
        if self.provider.lower() == "openai":
            return ChatOpenAI(
                api_key=settings.OPENAI_API_KEY,
                model=self.model,
                temperature=0.7,
            )
        elif self.provider.lower() == "anthropic":
            return Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        else:
            logger.warning(f"Unknown provider: {self.provider}, defaulting to OpenAI")
            return ChatOpenAI(
                api_key=settings.OPENAI_API_KEY,
                model=self.model,
                temperature=0.7,
            )

    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """Generate text using the LLM."""
        try:
            if self.provider.lower() == "openai":
                response = self.client.invoke(
                    [{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                return response.content
            elif self.provider.lower() == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": prompt}],
                )
                return response.content[0].text
            else:
                return "Unsupported provider"
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            raise
