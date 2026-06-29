"""Market and competitive analysis module."""

from typing import Dict, List, Any
import logging
from src.utils.llm_client import get_llm_client
from src.utils.formatters import OutputFormatter

logger = logging.getLogger(__name__)


class MarketAnalyzer:
    """Analyzes market trends and competitive landscape."""

    def __init__(self):
        self.llm = get_llm_client()
        self.formatter = OutputFormatter()

    def analyze_market(
        self,
        market: str,
        competitors: List[str] = None,
        trends: List[str] = None,
        focus_areas: List[str] = None,
    ) -> Dict[str, Any]:
        """Analyze overall market opportunity."""
        system_prompt = """You are an expert market analyst with deep knowledge of industry trends.
        Provide comprehensive market analysis including: size, growth potential, key trends,
        and emerging opportunities. Be data-driven and strategic."""

        user_message = f"""Analyze the {market} market.

Competitors: {', '.join(competitors) if competitors else 'None specified'}
Trends: {', '.join(trends) if trends else 'None specified'}
Focus Areas: {', '.join(focus_areas) if focus_areas else 'General analysis'}"""

        try:
            analysis = self.llm.generate_with_context(system_prompt, user_message)
            return {
                "market": market,
                "analysis": analysis,
                "competitors_analyzed": len(competitors) if competitors else 0,
                "status": "success",
            }
        except Exception as e:
            logger.error(f"Market analysis failed: {e}")
            return {"status": "error", "error": str(e)}

    def analyze_competitors(
        self, competitors: List[Dict[str, Any]], focus_areas: List[str] = None
    ) -> Dict[str, Any]:
        """Analyze competitive landscape."""
        system_prompt = """You are a competitive intelligence analyst.
        Analyze the provided competitors across key dimensions:
        - Strengths and weaknesses
        - Market positioning
        - Product differentiation
        - Pricing strategy
        - Go-to-market approach
        
        Provide strategic recommendations for competitive advantage."""

        user_message = f"""Analyze these competitors:

{chr(10).join(f'- {comp}' for comp in [c.get('name', str(c)) for c in competitors])}

Focus on: {', '.join(focus_areas) if focus_areas else 'Overall competitiveness'}"""

        try:
            analysis = self.llm.generate_with_context(system_prompt, user_message)
            return {
                "competitors_analyzed": len(competitors),
                "competitive_analysis": analysis,
                "status": "success",
            }
        except Exception as e:
            logger.error(f"Competitive analysis failed: {e}")
            return {"status": "error", "error": str(e)}

    def identify_market_gaps(
        self, market: str, existing_solutions: List[str] = None
    ) -> Dict[str, Any]:
        """Identify unmet needs and market gaps."""
        system_prompt = """You are an expert at identifying market opportunities.
        Analyze the market for unmet needs, underserved segments, and white space opportunities.
        Consider: customer pain points, emerging technologies, market trends, and demographic shifts."""

        user_message = f"""Identify market gaps in {market}.

Existing solutions: {', '.join(existing_solutions) if existing_solutions else 'None specified'}

What are the main gaps, underserved segments, and opportunities?"""

        try:
            gaps = self.llm.generate_with_context(system_prompt, user_message)
            return {
                "market": market,
                "identified_gaps": gaps,
                "status": "success",
            }
        except Exception as e:
            logger.error(f"Gap analysis failed: {e}")
            return {"status": "error", "error": str(e)}

    def analyze_trends(
        self, market: str, trends: List[str] = None
    ) -> Dict[str, Any]:
        """Analyze market and industry trends."""
        system_prompt = """You are a market trend analyst.
        Analyze the provided trends and explain their implications for product strategy.
        Consider: adoption rates, disruption potential, time horizons, and strategic importance."""

        user_message = f"""Analyze market trends in {market}.

Key trends to analyze: {', '.join(trends) if trends else 'Current market trends'}

What are the strategic implications and opportunities?"""

        try:
            trend_analysis = self.llm.generate_with_context(system_prompt, user_message)
            return {
                "market": market,
                "trend_analysis": trend_analysis,
                "trends_analyzed": len(trends) if trends else 0,
                "status": "success",
            }
        except Exception as e:
            logger.error(f"Trend analysis failed: {e}")
            return {"status": "error", "error": str(e)}
