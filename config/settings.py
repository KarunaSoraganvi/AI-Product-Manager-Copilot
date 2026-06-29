"""Configuration settings for the AI Product Manager Copilot."""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_DEBUG: bool = os.getenv("API_DEBUG", "True").lower() == "true"

    # LLM Configuration
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gpt-4")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Feature Flags
    ENABLE_WEB_SCRAPING: bool = os.getenv("ENABLE_WEB_SCRAPING", "False").lower() == "true"
    ENABLE_MARKET_INTELLIGENCE: bool = os.getenv("ENABLE_MARKET_INTELLIGENCE", "True").lower() == "true"

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = True


settings = Settings()
