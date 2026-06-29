"""Tests for the roadmap planner module."""

import pytest
from unittest.mock import patch, MagicMock
from src.modules.roadmap import RoadmapPlanner


@pytest.fixture
def planner():
    """Create roadmap planner instance for testing."""
    with patch("src.modules.roadmap.ChatOpenAI"):
        return RoadmapPlanner(model="gpt-4")


class TestRoadmapPlanner:
    """Test suite for RoadmapPlanner."""

    def test_planner_initialization(self, planner):
        """Test planner initializes correctly."""
        assert planner is not None
        assert planner.model_name == "gpt-4"
        assert planner.llm is not None

    def test_generate_roadmap(self, planner):
        """Test roadmap generation."""
        with patch.object(planner.llm, "invoke") as mock_invoke:
            mock_invoke.return_value = MagicMock(
                content='{"quarterly_roadmap": [], "milestones": []}'
            )
            
            result = planner.generate_roadmap(
                product_vision="AI-first product",
                goals=["Goal1"],
                features=[],
                timeline_quarters=4
            )
            
            assert result is not None
            assert isinstance(result, dict)

    def test_plan_release_schedule(self, planner):
        """Test release schedule planning."""
        with patch.object(planner.llm, "invoke") as mock_invoke:
            mock_invoke.return_value = MagicMock(
                content='{"releases": []}'
            )
            
            result = planner.plan_release_schedule(
                features=[],
                constraints={}
            )
            
            assert result is not None
            assert isinstance(result, dict)

    def test_scenario_planning(self, planner):
        """Test scenario planning."""
        with patch.object(planner.llm, "invoke") as mock_invoke:
            mock_invoke.return_value = MagicMock(
                content='{"scenarios": []}'
            )
            
            result = planner.scenario_planning(
                base_roadmap={},
                scenarios=["Growth", "Decline"]
            )
            
            assert result is not None
            assert isinstance(result, dict)
