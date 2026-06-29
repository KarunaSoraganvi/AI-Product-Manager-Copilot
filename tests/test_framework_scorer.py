"""Tests for the feature prioritization framework scorer."""

import pytest
from unittest.mock import patch, MagicMock
from src.core.framework_scorer import FeatureScorer


@pytest.fixture
def scorer():
    """Create feature scorer instance for testing."""
    with patch("src.core.framework_scorer.ChatOpenAI"):
        return FeatureScorer(model="gpt-4")


class TestFeatureScorer:
    """Test suite for FeatureScorer."""

    def test_scorer_initialization(self, scorer):
        """Test scorer initializes correctly."""
        assert scorer is not None
        assert scorer.model_name == "gpt-4"
        assert scorer.llm is not None

    def test_score_by_rice(self, scorer):
        """Test RICE scoring."""
        with patch.object(scorer.llm, "invoke") as mock_invoke:
            mock_invoke.return_value = MagicMock(
                content='[{"name": "Feature1", "rice_score": 100, "rank": 1}]'
            )
            
            features = [
                {"name": "Feature1", "reach": 1000, "impact": 3, "confidence": 0.8, "effort": 5}
            ]
            result = scorer.score_by_rice(features)
            
            assert result is not None
            assert isinstance(result, list)

    def test_score_by_moscow(self, scorer):
        """Test MoSCoW scoring."""
        with patch.object(scorer.llm, "invoke") as mock_invoke:
            mock_invoke.return_value = MagicMock(
                content='{"must": [{"name": "Feature1"}], "should": [], "could": [], "wont": []}'
            )
            
            features = [{"name": "Feature1"}]
            result = scorer.score_by_moscow(features)
            
            assert result is not None
            assert isinstance(result, dict)
            assert "must" in result or "should" in result

    def test_score_by_value_effort(self, scorer):
        """Test Value vs Effort scoring."""
        with patch.object(scorer.llm, "invoke") as mock_invoke:
            mock_invoke.return_value = MagicMock(
                content='[{"name": "Feature1", "value": 8, "effort": 3}]'
            )
            
            features = [{"name": "Feature1"}]
            result = scorer.score_by_value_effort(features)
            
            assert result is not None
            assert isinstance(result, list)
