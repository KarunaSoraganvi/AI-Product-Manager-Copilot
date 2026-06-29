"""Feature prioritization framework scorer."""

import logging
from typing import Any, Dict, List
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from config.settings import settings

logger = logging.getLogger(__name__)


class FeatureScorer:
    """Scores and ranks features using various frameworks."""

    FRAMEWORKS = ["RICE", "MoSCoW", "VALUE_EFFORT", "KANO", "WEIGHTED_SCORE"]

    def __init__(self, model: str = None):
        """Initialize the feature scorer."""
        self.model_name = model or settings.DEFAULT_MODEL
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=self.model_name,
            temperature=0.5,
        )
        logger.info(f"Initialized FeatureScorer with model: {self.model_name}")

    def score_by_rice(self, features: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Score features using RICE framework (Reach, Impact, Confidence, Effort)."""
        features_str = json.dumps(features, indent=2)
        
        prompt = PromptTemplate(
            input_variables=["features"],
            template="""Score each feature using the RICE framework:
- Reach: How many users will this affect (monthly)
- Impact: How much will this impact each user (3x, 2x, 1x, 0.5x, 0.25x)
- Confidence: How confident are we (0-1)
- Effort: How many person-weeks

Formula: RICE Score = (Reach × Impact × Confidence) / Effort

Features:
{features}

For each feature provide:
1. Reach estimate
2. Impact multiplier
3. Confidence score
4. Effort estimate
5. RICE score
6. Rank

Provide response as JSON array sorted by RICE score descending.""",
        )

        chain = prompt | self.llm
        response = chain.invoke({"features": features_str})
        
        try:
            scored = json.loads(response.content)
        except json.JSONDecodeError:
            scored = features
        
        return scored

    def score_by_moscow(self, features: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Score features using MoSCoW method (Must, Should, Could, Won't)."""
        features_str = json.dumps(features, indent=2)
        
        prompt = PromptTemplate(
            input_variables=["features"],
            template="""Categorize each feature using the MoSCoW method:
- Must: Critical for success
- Should: Important but not critical
- Could: Nice to have
- Won't: Out of scope for now

Features:
{features}

For each feature provide:
1. Feature name
2. Category (Must/Should/Could/Won't)
3. Justification
4. Dependencies

Provide response as JSON with structure:
{{
  "must": [...],
  "should": [...],
  "could": [...],
  "wont": [...]
}}""",
        )

        chain = prompt | self.llm
        response = chain.invoke({"features": features_str})
        
        try:
            categorized = json.loads(response.content)
        except json.JSONDecodeError:
            categorized = {"must": [], "should": features, "could": [], "wont": []}
        
        return categorized

    def score_by_value_effort(self, features: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Score features by value vs effort (2x2 matrix)."""
        features_str = json.dumps(features, indent=2)
        
        prompt = PromptTemplate(
            input_variables=["features"],
            template="""Evaluate each feature on value vs effort:
- Value: Business and user value (1-10)
- Effort: Development effort required (1-10)

Quadrants:
- Quick wins: High value, low effort
- Strategic: High value, high effort
- Maybes: Low value, low effort
- Time wasters: Low value, high effort

Features:
{features}

For each feature provide:
1. Feature name
2. Value score (1-10)
3. Effort score (1-10)
4. Quadrant
5. Recommendation

Provide response as JSON array.""",
        )

        chain = prompt | self.llm
        response = chain.invoke({"features": features_str})
        
        try:
            scored = json.loads(response.content)
        except json.JSONDecodeError:
            scored = features
        
        return scored

    def score_by_framework(self, features: List[Dict[str, Any]], framework: str = "RICE", weights: Dict[str, float] = None) -> List[Dict[str, Any]]:
        """Score features using specified framework."""
        framework = framework.upper()
        
        if framework not in self.FRAMEWORKS:
            logger.warning(f"Unknown framework: {framework}, using RICE")
            framework = "RICE"
        
        if framework == "RICE":
            return self.score_by_rice(features)
        elif framework == "MOSCOW":
            return self.score_by_moscow(features)
        elif framework == "VALUE_EFFORT":
            return self.score_by_value_effort(features)
        else:
            return features
