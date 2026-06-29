"""LLM client for interfacing with different AI models."""

from typing import Optional, List, Dict, Any
import logging
from abc import ABC, abstractmethod

from openai import OpenAI, AsyncOpenAI
from anthropic import Anthropic

from config.settings import settings

logger = logging.getLogger(__name__)


class LLMClient(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from prompt."""
        pass

    @abstractmethod
    def generate_with_context(
        self, system_prompt: str, user_message: str, **kwargs
    ) -> str:
        """Generate text with system context."""
        pass


class OpenAIClient(LLMClient):
    """Client for OpenAI API."""

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.temperature = settings.OPENAI_TEMPERATURE

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from prompt using OpenAI."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", self.temperature),
                max_tokens=kwargs.get("max_tokens", settings.MAX_OUTPUT_TOKENS),
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise

    def generate_with_context(
        self, system_prompt: str, user_message: str, **kwargs
    ) -> str:
        """Generate text with system context using OpenAI."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=kwargs.get("temperature", self.temperature),
                max_tokens=kwargs.get("max_tokens", settings.MAX_OUTPUT_TOKENS),
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise


class AnthropicClient(LLMClient):
    """Client for Anthropic API."""

    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.ANTHROPIC_MODEL

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from prompt using Anthropic."""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=kwargs.get("max_tokens", settings.MAX_OUTPUT_TOKENS),
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise

    def generate_with_context(
        self, system_prompt: str, user_message: str, **kwargs
    ) -> str:
        """Generate text with system context using Anthropic."""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=kwargs.get("max_tokens", settings.MAX_OUTPUT_TOKENS),
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise


def get_llm_client() -> LLMClient:
    """Factory function to get appropriate LLM client."""
    provider = settings.LLM_PROVIDER.lower()

    if provider == "openai":
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not configured")
        return OpenAIClient()
    elif provider == "anthropic":
        if not settings.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not configured")
        return AnthropicClient()
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
