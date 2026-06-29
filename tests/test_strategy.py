"""Tests for the strategy developer module."""

import pytest
from unittest.mock import patch, MagicMock
from src.modules.strategy import StrategyDeveloper


@pytest.fixture
def developer():
    """Create strategy developer instance for testing."""
    with patch("src.modules.strategy.ChatOpenAI"):
        return StrategyDeveloper(model="gpt-4")


class TestStrategyDeveloper:
    """Test suite for StrategyDeveloper."""

    def test_developer_initialization(self, developer):
        """Test developer initializes correctly."""
        assert developer is not None
        assert developer.model_name == "gpt-4"
        assert developer.llm is not None

    def test_develop_strategy(self, developer):
        """Test strategy development."""
        with patch.object(developer.llm, "invoke") as mock_invoke:
            mock_invoke.return_value = MagicMock(
                content='{"vision": "Test vision", "pillars": []}'
            )
            
            result = developer.develop_strategy(
                context={"market": "SaaS"},
                objectives=["Objective1"]
            )
            
            assert result is not None
            assert isinstance(result, dict)

    def test_gtm_planning(self, developer):
        """Test GTM planning."""
        with patch.object(developer.llm, "invoke") as mock_invoke:
            mock_invoke.return_value = MagicMock(
                content='{"gtm": {}}'
            )
            
            result = developer.gtm_planning(
                product_info={"name": "Product"},
                market_info={"size": "$10B"}
            )
            
            assert result is not None
            assert isinstance(result, dict)

    def test_stakeholder_alignment(self, developer):
        """Test stakeholder alignment."""
        with patch.object(developer.llm, "invoke") as mock_invoke:
            mock_invoke.return_value = MagicMock(
                content='{"alignment": []}'
            )
            
            result = developer.stakeholder_alignment(
                strategy={},
                stakeholders=[{"name": "CEO", "role": "Executive"}]
            )
            
            assert result is not None
            assert isinstance(result, dict)
