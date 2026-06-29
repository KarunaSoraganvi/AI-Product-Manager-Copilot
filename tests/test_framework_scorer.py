"""Tests for feature scoring framework."""

import pytest
from src.core.framework_scorer import FeatureScorer


class TestFeatureScorer:
    """Test suite for feature prioritization."""

    @pytest.fixture
    def sample_features(self):
        """Sample features for testing."""
        return [
            {
                "name": "Feature A",
                "reach": 100,
                "impact": 3,
                "confidence": 80,
                "effort": 5,
            },
            {
                "name": "Feature B",
                "reach": 50,
                "impact": 4,
                "confidence": 90,
                "effort": 2,
            },
            {
                "name": "Feature C",
                "reach": 200,
                "impact": 2,
                "confidence": 70,
                "effort": 10,
            },
        ]

    def test_rice_scoring(self, sample_features):
        """Test RICE framework scoring."""
        scored = FeatureScorer.score_rice(sample_features)

        assert len(scored) == len(sample_features)
        assert "rice_score" in scored[0]
        # Verify sorted by score descending
        assert scored[0]["rice_score"] >= scored[-1]["rice_score"]

    def test_moscow_scoring(self):
        """Test MoSCoW framework scoring."""
        features = [
            {"name": "Feature A", "moscow_priority": "Must"},
            {"name": "Feature B", "moscow_priority": "Should"},
            {"name": "Feature C", "moscow_priority": "Could"},
        ]

        scored = FeatureScorer.score_moscow(features)

        assert len(scored) == 3
        assert scored[0]["moscow_score"] == 4  # Must
        assert scored[1]["moscow_score"] == 3  # Should
        assert scored[2]["moscow_score"] == 2  # Could

    def test_value_effort_quadrant(self):
        """Test Value vs Effort quadrant classification."""
        assert (
            FeatureScorer._get_quadrant(8, 2) == "Quick Wins"
        )
        assert (
            FeatureScorer._get_quadrant(8, 8) == "Major Projects"
        )
        assert (
            FeatureScorer._get_quadrant(2, 2) == "Fill Ins"
        )
        assert (
            FeatureScorer._get_quadrant(2, 8) == "Time Sinks"
        )


if __name__ == "__main__":
    pytest.main([__file__])
