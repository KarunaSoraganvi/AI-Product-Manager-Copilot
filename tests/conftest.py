"""Test configuration and fixtures."""

import pytest
import os
from unittest.mock import patch, MagicMock

# Set test environment
os.environ["OPENAI_API_KEY"] = "test-key-123"
os.environ["LLM_PROVIDER"] = "openai"
os.environ["DEFAULT_MODEL"] = "gpt-4"


@pytest.fixture
def mock_llm():
    """Mock LLM for testing without real API calls."""
    with patch("src.core.analyzer.ChatOpenAI") as mock:
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = MagicMock(content='{"result": "test"}')
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_env():
    """Set up mock environment variables."""
    with patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-key",
        "LLM_PROVIDER": "openai",
        "DEFAULT_MODEL": "gpt-4"
    }):
        yield
