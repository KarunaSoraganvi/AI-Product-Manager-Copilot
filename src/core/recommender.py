"""Recommendation engine for product decisions."""

import logging
from typing import Any, Dict, List
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from config.settings import settings

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """Generates recommendations based on analysis and constraints."""

    def __init__(self, model: str = None):
        """Initialize the recommendation engine."""
        self.model_name = model or settings.DEFAULT_MODEL
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=self.model_name,
            temperature=0.7,
        )
        logger.info(f"Initialized RecommendationEngine with model: {self.model_name}")

    def recommend_features(self, context: Dict[str, Any], constraints: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Recommend features based on market analysis and user research."""
        constraints = constraints or {}
        context_str = json.dumps(context, indent=2)
        constraints_str = json.dumps(constraints, indent=2)
        
        prompt = PromptTemplate(
            input_variables=["context", "constraints"],
            template="""Based on the following context and constraints, recommend 5-7 product features.
For each feature provide:
1. Feature name
2. Description
3. User value
4. Implementation complexity (low/medium/high)
5. Timeline estimate (weeks)
6. Expected impact (ROI)

Context:
{context}

Constraints:
{constraints}

Provide response as JSON array.""",
        )

        chain = prompt | self.llm
        response = chain.invoke({"context": context_str, "constraints": constraints_str})
        
        try:
            recommendations = json.loads(response.content)
        except json.JSONDecodeError:
            recommendations = [{"feature": "analysis", "description": response.content}]
        
        return recommendations if isinstance(recommendations, list) else [recommendations]

    def recommend_positioning(self, market_analysis: Dict[str, Any], competitive_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend product positioning strategy."""
        prompt = PromptTemplate(
            input_variables=["market", "competition"],
            template="""Based on market and competitive analysis, recommend:
1. Target market segment
2. Unique value proposition
3. Key differentiators
4. Pricing strategy
5. Go-to-market approach
6. Brand positioning

Market Analysis:
{market}

Competitive Analysis:
{competition}

Provide response as JSON.""",
        )

        chain = prompt | self.llm
        market_str = json.dumps(market_analysis, indent=2)
        comp_str = json.dumps(competitive_analysis, indent=2)
        response = chain.invoke({"market": market_str, "competition": comp_str})
        
        try:
            result = json.loads(response.content)
        except json.JSONDecodeError:
            result = {"positioning": response.content}
        
        return result

    def recommend_priorities(self, items: List[Dict[str, Any]], weights: Dict[str, float] = None) -> List[Dict[str, Any]]:
        """Recommend priority ordering for items."""
        weights = weights or {"impact": 0.4, "effort": 0.3, "urgency": 0.3}
        items_str = json.dumps(items, indent=2)
        weights_str = json.dumps(weights, indent=2)
        
        prompt = PromptTemplate(
            input_variables=["items", "weights"],
            template="""Prioritize the following items using the specified weights:
Weights:
{weights}

Items:
{items}

For each item, provide:
1. Rank
2. Justification
3. Dependencies
4. Recommended timeline

Provide response as JSON array.""",
        )

        chain = prompt | self.llm
        response = chain.invoke({"items": items_str, "weights": weights_str})
        
        try:
            recommendations = json.loads(response.content)
        except json.JSONDecodeError:
            recommendations = items
        
        return recommendations
