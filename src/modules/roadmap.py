"""Roadmap generation and planning module."""

import logging
from typing import Any, Dict, List
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from config.settings import settings

logger = logging.getLogger(__name__)


class RoadmapPlanner:
    """Generates and optimizes product roadmaps."""

    def __init__(self, model: str = None):
        """Initialize the roadmap planner."""
        self.model_name = model or settings.DEFAULT_MODEL
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=self.model_name,
            temperature=0.7,
        )
        logger.info(f"Initialized RoadmapPlanner with model: {self.model_name}")

    def generate_roadmap(self, product_vision: str, goals: List[str], features: List[Dict[str, Any]], timeline_quarters: int = 4) -> Dict[str, Any]:
        """Generate a strategic product roadmap."""
        goals_str = "\n".join([f"- {g}" for g in goals])
        features_str = json.dumps(features, indent=2)
        
        prompt = PromptTemplate(
            input_variables=["vision", "goals", "features", "timeline"],
            template="""Create a {timeline}-quarter product roadmap.

Product Vision:
{vision}

Strategic Goals:
{goals}

Available Features:
{features}

For the roadmap:
1. Define quarterly themes
2. Allocate features to quarters
3. Identify dependencies
4. Estimate effort for each quarter
5. Establish success metrics
6. Plan releases and milestones
7. Risk mitigation strategies

Provide response as JSON with:
- quarterly_roadmap: array of quarters with themes and features
- milestones: key deliverables
- dependencies: feature dependencies
- success_metrics: how to measure success
- risks: identified risks and mitigation
- resource_plan: team structure and capacity
""",
        )

        chain = prompt | self.llm
        response = chain.invoke({
            "vision": product_vision,
            "goals": goals_str,
            "features": features_str,
            "timeline": timeline_quarters
        })
        
        try:
            result = json.loads(response.content)
        except json.JSONDecodeError:
            result = {"roadmap": response.content, "quarters": timeline_quarters}
        
        return result

    def plan_release_schedule(self, features: List[Dict[str, Any]], constraints: Dict[str, Any] = None) -> Dict[str, Any]:
        """Plan release schedule and sequencing."""
        constraints = constraints or {}
        features_str = json.dumps(features, indent=2)
        constraints_str = json.dumps(constraints, indent=2)
        
        prompt = PromptTemplate(
            input_variables=["features", "constraints"],
            template="""Plan a release schedule for these features:

Features:
{features}

Constraints:
{constraints}

For the release plan provide:
1. Release sequencing
   - Dependencies
   - Critical path
   - Parallel workstreams

2. Release timeline
   - Proposed dates
   - Sprint allocation
   - Buffer time

3. Release content
   - Feature grouping
   - Release themes
   - Communication story

4. Risk assessment
   - Technical risks
   - Market risks
   - Mitigation strategies

5. Success criteria
   - Launch metrics
   - Post-launch monitoring
   - Rollback criteria

Provide response as JSON.""",
        )

        chain = prompt | self.llm
        response = chain.invoke({"features": features_str, "constraints": constraints_str})
        
        try:
            result = json.loads(response.content)
        except json.JSONDecodeError:
            result = {"release_plan": response.content}
        
        return result

    def scenario_planning(self, base_roadmap: Dict[str, Any], scenarios: List[str]) -> Dict[str, Any]:
        """Plan roadmap scenarios based on different conditions."""
        roadmap_str = json.dumps(base_roadmap, indent=2)
        scenarios_str = "\n".join([f"- {s}" for s in scenarios])
        
        prompt = PromptTemplate(
            input_variables=["roadmap", "scenarios"],
            template="""Create roadmap scenarios for these conditions:

Base Roadmap:
{roadmap}

Scenarios:
{scenarios}

For each scenario provide:
1. Scenario description
2. Key adjustments to roadmap
3. Feature prioritization changes
4. Timeline impacts
5. Resource needs
6. Success metrics
7. Trigger conditions to activate

Also provide:
- Scenario probabilities
- Leading indicators to watch
- Contingency triggers
- Decision points

Provide response as JSON.""",
        )

        chain = prompt | self.llm
        response = chain.invoke({"roadmap": roadmap_str, "scenarios": scenarios_str})
        
        try:
            result = json.loads(response.content)
        except json.JSONDecodeError:
            result = {"scenarios": scenarios, "planning": response.content}
        
        return result
