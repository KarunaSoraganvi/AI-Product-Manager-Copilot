"""Tests for the data analyzer."""

import pytest
from src.core.analyzer import DataAnalyzer


@pytest.fixture
def analyzer():
    """Create analyzer instance for testing."""
    return DataAnalyzer(model="gpt-4")


def test_analyzer_initialization(analyzer):
    """Test analyzer initialization."""
    assert analyzer is not None
    assert analyzer.model_name == "gpt-4"


def test_sentiment_analysis(analyzer):
    """Test sentiment analysis."""
    result = analyzer.analyze_sentiment("This product is amazing and I love it!")
    assert "sentiment" in result
    assert "confidence" in result or "polarity" in result
