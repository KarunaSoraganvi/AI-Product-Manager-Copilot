"""Tests for the core data analyzer."""

import pytest
import json
from unittest.mock import patch, MagicMock
from src.core.analyzer import DataAnalyzer


@pytest.fixture
def analyzer():
    """Create analyzer instance for testing."""
    with patch("src.core.analyzer.ChatOpenAI"):
        return DataAnalyzer(model="gpt-4")


class TestDataAnalyzer:
    """Test suite for DataAnalyzer."""

    def test_analyzer_initialization(self, analyzer):
        """Test analyzer initializes correctly."""
        assert analyzer is not None
        assert analyzer.model_name == "gpt-4"
        assert analyzer.llm is not None

    def test_analyze_sentiment(self, analyzer):
        """Test sentiment analysis."""
        with patch.object(analyzer.llm, "invoke") as mock_invoke:
            mock_invoke.return_value = MagicMock(
                content='{"sentiment": "positive", "confidence": 0.9}'
            )
            
            result = analyzer.analyze_sentiment("This is amazing!")
            
            assert result is not None
            assert isinstance(result, dict)

    def test_extract_key_themes(self, analyzer):
        """Test theme extraction."""
        with patch.object(analyzer.llm, "invoke") as mock_invoke:
            mock_invoke.return_value = MagicMock(
                content='{"themes": ["theme1", "theme2"]}'
            )
            
            data = ["point 1", "point 2"]
            result = analyzer.extract_key_themes(data)
            
            assert result is not None
            assert isinstance(result, dict)

    def test_synthesize_insights(self, analyzer):
        """Test insight synthesis."""
        with patch.object(analyzer.llm, "invoke") as mock_invoke:
            mock_invoke.return_value = MagicMock(
                content='{"insights": ["insight1", "insight2"]}'
            )
            
            analysis = [{"key": "value"}]
            result = analyzer.synthesize_insights(analysis)
            
            assert result is not None
            assert isinstance(result, dict)
