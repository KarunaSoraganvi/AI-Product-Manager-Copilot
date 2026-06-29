"""Tests for the market analyzer module."""

import pytest
from unittest.mock import patch, MagicMock
from src.modules.market_analysis import MarketAnalyzer


@pytest.fixture
def market_analyzer():
    """Create market analyzer instance for testing."""
    with patch("src.modules.market_analysis.ChatOpenAI"):
        return MarketAnalyzer(model="gpt-4")


class TestMarketAnalyzer:
    """Test suite for MarketAnalyzer."""

    def test_analyzer_initialization(self, market_analyzer):
        """Test market analyzer initializes correctly."""
        assert market_analyzer is not None
        assert market_analyzer.model_name == "gpt-4"
        assert market_analyzer.llm is not None

    def test_analyze_market(self, market_analyzer):
        """Test market analysis."""
        with patch.object(market_analyzer.llm, "invoke") as mock_invoke:
            mock_invoke.return_value = MagicMock(
                content='{"market_size": "$10B", "trends": []}'
            )
            
            result = market_analyzer.analyze_market(
                market="SaaS",
                competitors=["Competitor1"],
                focus_areas=["trends"]
            )
            
            assert result is not None
            assert isinstance(result, dict)

    def test_analyze_competitors(self, market_analyzer):
        """Test competitor analysis."""
        with patch.object(market_analyzer.llm, "invoke") as mock_invoke:
            mock_invoke.return_value = MagicMock(
                content='{"competitors": {"Asana": {"strengths": []}}}'
            )
            
            result = market_analyzer.analyze_competitors(
                competitors=["Asana", "Monday.com"]
            )
            
            assert result is not None
            assert isinstance(result, dict)

    def test_identify_market_gaps(self, market_analyzer):
        """Test market gap identification."""
        with patch.object(market_analyzer.llm, "invoke") as mock_invoke:
            mock_invoke.return_value = MagicMock(
                content='{"gaps": [{"description": "Gap1"}]}'
            )
            
            result = market_analyzer.identify_market_gaps(
                market="SaaS",
                competitors=["Asana"],
                features=["Feature1"]
            )
            
            assert result is not None
            assert isinstance(result, dict)
