"""Market analysis module for competitive intelligence and market research."""

import logging
from typing import Any, Dict, List
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from config.settings import settings

logger = logging.getLogger(__name__)


class MarketAnalyzer:
    """Analyzes market trends, competition, and opportunities."""

    def __init__(self, model: str = None):
        """Initialize the market analyzer."""
        self.model_name = model or settings.DEFAULT_MODEL
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=self.model_name,
            temperature=0.7,
        )
        logger.info(f"Initialized MarketAnalyzer with model: {self.model_name}")

    def analyze_market(self, market: str, competitors: List[str] = None, focus_areas: List[str] = None) -> Dict[str, Any]:
        """Perform comprehensive market analysis."""
        competitors = competitors or []
        focus_areas = focus_areas or ["trends", "opportunities", "threats", "market_size"]
        
        prompt = PromptTemplate(
            input_variables=["market", "competitors", "focus"],
            template="""Analyze the {market} market. Provide:

1. Market Size & Growth
   - Current market size
   - Growth rate
   - Projected growth

2. Market Trends
   - Top 3 trends
   - Emerging technologies
   - Consumer behavior shifts

3. Opportunities
   - Market gaps
   - Underserved segments
   - New applications

4. Threats
   - Regulatory risks
   - Competitive pressures
   - Economic factors

5. Key Success Factors
   - Critical capabilities
   - Customer requirements
   - Competitive advantages

Competitors to analyze: {competitors}
Focus areas: {focus}

Provide response as JSON.""",
        )

        chain = prompt | self.llm
        response = chain.invoke({
            "market": market,
            "competitors": ", ".join(competitors) if competitors else "major players",
            "focus": ", ".join(focus_areas)
        })
        
        try:
            result = json.loads(response.content)
        except json.JSONDecodeError:
            result = {"analysis": response.content, "market": market}
        
        return result

    def analyze_competitors(self, competitors: List[str], focus_areas: List[str] = None) -> Dict[str, Any]:
        """Analyze competitive landscape."""
        focus_areas = focus_areas or ["features", "pricing", "strengths", "weaknesses", "positioning"]
        competitors_str = "\n".join([f"- {c}" for c in competitors])
        
        prompt = PromptTemplate(
            input_variables=["competitors", "focus"],
            template="""Perform competitive analysis for these products:
{competitors}

For each competitor analyze:
1. Core Features & Capabilities
2. Pricing Model & Structure
3. Target Market
4. Strengths & Competitive Advantages
5. Weaknesses & Limitations
6. Market Position
7. Recent Updates & Roadmap

Focus areas: {focus}

Also provide:
- Competitive positioning matrix
- Gap analysis
- Differentiation opportunities

Provide response as JSON.""",
        )

        chain = prompt | self.llm
        response = chain.invoke({"competitors": competitors_str, "focus": ", ".join(focus_areas)})
        
        try:
            result = json.loads(response.content)
        except json.JSONDecodeError:
            result = {"competitors": competitors, "analysis": response.content}
        
        return result

    def identify_market_gaps(self, market: str, competitors: List[str], features: List[str] = None) -> Dict[str, Any]:
        """Identify unmet needs and market gaps."""
        prompt = PromptTemplate(
            input_variables=["market", "competitors", "features"],
            template="""Identify market gaps in the {market} market.

Analyze gaps in terms of:
1. Functionality gaps
   - Missing features
   - Unmet customer needs
   - Pain points not addressed

2. Market segment gaps
   - Underserved user segments
   - Geographic opportunities
   - Use case gaps

3. Experience gaps
   - Usability issues
   - Integration challenges
   - Customer experience problems

4. Pricing gaps
   - Affordability issues
   - Licensing models
   - Value perception

Competitors: {competitors}
Known features: {features}

For each gap provide:
1. Description
2. Size & potential
3. Difficulty to address
4. ROI potential

Provide response as JSON.""",
        )

        chain = prompt | self.llm
        response = chain.invoke({
            "market": market,
            "competitors": ", ".join(competitors),
            "features": ", ".join(features) if features else "various"
        })
        
        try:
            result = json.loads(response.content)
        except json.JSONDecodeError:
            result = {"gaps": response.content}
        
        return result
