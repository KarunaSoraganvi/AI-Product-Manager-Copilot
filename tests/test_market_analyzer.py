"""Tests for market analyzer."""

import pytest
from src.modules.market_analysis import MarketAnalyzer


@pytest.fixture
def analyzer():
    """Create analyzer instance for testing."""
    return MarketAnalyzer(model="gpt-4")


def test_analyzer_initialization(analyzer):
    """Test analyzer initialization."""
    assert analyzer is not None
    assert analyzer.model_name == "gpt-4"
