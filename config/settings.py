"""Configuration settings for AI Product Manager Copilot."""

from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_DEBUG: bool = False

    # LLM Configuration
    LLM_PROVIDER: str = "openai"  # Options: openai, anthropic, local
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_TEMPERATURE: float = 0.7

    ANTHROPIC_API_KEY: Optional[str] = None
    ANTHROPIC_MODEL: str = "claude-3-opus-20240229"

    # Feature Flags
    ENABLE_MARKET_ANALYSIS: bool = True
    ENABLE_USER_RESEARCH: bool = True
    ENABLE_ROADMAP_PLANNING: bool = True
    ENABLE_STRATEGY_GENERATION: bool = True
    ENABLE_COMPETITIVE_ANALYSIS: bool = True

    # Analysis Parameters
    MAX_CONTEXT_TOKENS: int = 8000
    MAX_OUTPUT_TOKENS: int = 2000
    PRIORITIZATION_FRAMEWORK: str = "RICE"  # RICE, MoSCoW, Kano

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json or standard

    # Data Processing
    MAX_FILE_SIZE_MB: int = 50
    SUPPORTED_FILE_TYPES: list = ["csv", "json", "txt", "pdf"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
