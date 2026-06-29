"""Tests for the recommendation engine."""

import pytest
from unittest.mock import patch, MagicMock
from src.core.recommender import RecommendationEngine


@pytest.fixture
def recommender():
    """Create recommendation engine instance for testing."""
    with patch("src.core.recommender.ChatOpenAI"):
        return RecommendationEngine(model="gpt-4")


class TestRecommendationEngine:
    """Test suite for RecommendationEngine."""

    def test_engine_initialization(self, recommender):
        """Test recommendation engine initializes correctly."""
        assert recommender is not None
        assert recommender.model_name == "gpt-4"
        assert recommender.llm is not None

    def test_recommend_features(self, recommender):
        """Test feature recommendation."""
        with patch.object(recommender.llm, "invoke") as mock_invoke:
            mock_invoke.return_value = MagicMock(
                content='[{"feature": "Feature1"}]'
            )
            
            result = recommender.recommend_features(
                context={"market": "SaaS"},
                constraints={}
            )
            
            assert result is not None
            assert isinstance(result, list)

    def test_recommend_positioning(self, recommender):
        """Test positioning recommendation."""
        with patch.object(recommender.llm, "invoke") as mock_invoke:
            mock_invoke.return_value = MagicMock(
                content='{"positioning": "Positioning strategy"}'
            )
            
            result = recommender.recommend_positioning(
                market_analysis={},
                competitive_analysis={}
            )
            
            assert result is not None
            assert isinstance(result, dict)

    def test_recommend_priorities(self, recommender):
        """Test priority recommendation."""
        with patch.object(recommender.llm, "invoke") as mock_invoke:
            mock_invoke.return_value = MagicMock(
                content='[{"item": "Item1", "rank": 1}]'
            )
            
            result = recommender.recommend_priorities(
                items=[{"name": "Item1"}],
                weights={"impact": 0.5}
            )
            
            assert result is not None
            assert isinstance(result, list)
