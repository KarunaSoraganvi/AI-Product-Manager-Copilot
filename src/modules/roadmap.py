"""Product roadmap generation and planning module."""

from typing import Dict, List, Any
import logging
from src.utils.llm_client import get_llm_client

logger = logging.getLogger(__name__)


class RoadmapPlanner:
    """Generates and optimizes product roadmaps."""

    def __init__(self):
        self.llm = get_llm_client()

    def generate_roadmap(
        self,
        product_vision: str,
        goals: List[str],
        features: List[Dict[str, Any]],
        timeline_quarters: int = 4,
        constraints: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Generate a strategic product roadmap."""
        system_prompt = """You are an expert product manager and strategist.
        Create a detailed, actionable product roadmap that:
        - Aligns with the product vision and strategic goals
        - Prioritizes high-impact features
        - Considers resource constraints and dependencies
        - Includes clear phases with milestones
        - Balances innovation with stability
        
        Format as clear phases with timelines and deliverables."""

        features_str = "\n".join(
            [f"- {f.get('name', 'Feature')}: {f.get('description', '')}" for f in features]
        )

        constraints_str = (
            "\n".join(f"- {k}: {v}" for k, v in constraints.items())
            if constraints
            else "None specified"
        )

        user_message = f"""Create a {timeline_quarters}-quarter product roadmap for a product with:

Vision: {product_vision}

Strategic Goals:
{chr(10).join(f'- {goal}' for goal in goals)}

Candidate Features:
{features_str}

Constraints:
{constraints_str}

Generate a prioritized roadmap with phases, milestones, and success metrics."""

        try:
            roadmap = self.llm.generate_with_context(system_prompt, user_message)
            return {
                "product_vision": product_vision,
                "roadmap": roadmap,
                "timeline_quarters": timeline_quarters,
                "features_considered": len(features),
                "status": "success",
            }
        except Exception as e:
            logger.error(f"Roadmap generation failed: {e}")
            return {"status": "error", "error": str(e)}

    def plan_phases(
        self, goals: List[str], dependencies: Dict[str, List[str]] = None
    ) -> Dict[str, Any]:
        """Plan execution phases considering dependencies."""
        system_prompt = """You are a project planning expert.
        Create clear execution phases that:
        - Respect dependencies between work items
        - Sequence work logically
        - Include milestones and success criteria
        - Identify critical path
        - Account for parallel workstreams"""

        deps_str = (
            "\n".join(
                f"- {item}: depends on {', '.join(deps)}" for item, deps in dependencies.items()
            )
            if dependencies
            else "No known dependencies"
        )

        user_message = f"""Plan execution phases for these goals:

{chr(10).join(f'- {goal}' for goal in goals)}

Dependencies:
{deps_str}

Provide a phased execution plan with timelines and dependencies."""

        try:
            phases = self.llm.generate_with_context(system_prompt, user_message)
            return {
                "execution_phases": phases,
                "goals_count": len(goals),
                "status": "success",
            }
        except Exception as e:
            logger.error(f"Phase planning failed: {e}")
            return {"status": "error", "error": str(e)}

    def analyze_roadmap_scenarios(
        self, scenarios: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze different roadmap scenarios."""
        system_prompt = """You are a scenario planning expert.
        Compare and analyze the provided roadmap scenarios.
        Evaluate: feasibility, risk, resource requirements, timeline, and strategic alignment.
        Provide a recommendation with pros/cons of each."""

        scenario_str = "\n\n".join(
            [
                f"Scenario {i+1}: {s.get('name', f'Scenario {i+1}')}\n{s.get('description', '')}"
                for i, s in enumerate(scenarios)
            ]
        )

        user_message = f"""Analyze these roadmap scenarios:

{scenario_str}

Compare across: feasibility, risk, resources, timeline, and strategic alignment."""

        try:
            analysis = self.llm.generate_with_context(system_prompt, user_message)
            return {
                "scenarios_analyzed": len(scenarios),
                "scenario_analysis": analysis,
                "status": "success",
            }
        except Exception as e:
            logger.error(f"Scenario analysis failed: {e}")
            return {"status": "error", "error": str(e)}
