"""Strategy development and planning module."""

from typing import Dict, List, Any
import logging
from src.utils.llm_client import get_llm_client

logger = logging.getLogger(__name__)


class StrategyDeveloper:
    """Develops product and go-to-market strategies."""

    def __init__(self):
        self.llm = get_llm_client()

    def develop_product_strategy(
        self,
        company_vision: str,
        market_opportunity: str,
        competitive_landscape: str,
        internal_capabilities: List[str],
    ) -> Dict[str, Any]:
        """Develop comprehensive product strategy."""
        system_prompt = """You are a strategic product leader.
        Develop a comprehensive product strategy that includes:
        - Clear value proposition and differentiation
        - Target market and customer segments
        - Strategic positioning vs competitors
        - Product vision and North Star metrics
        - Key strategic initiatives
        - Success criteria and KPIs
        - 12-month strategic roadmap
        
        Make it actionable and specific to the context."""

        user_message = f"""Develop a product strategy with:

Company Vision: {company_vision}

Market Opportunity: {market_opportunity}

Competitive Landscape: {competitive_landscape}

Our Capabilities: {', '.join(internal_capabilities)}

Create a comprehensive, actionable product strategy."""

        try:
            strategy = self.llm.generate_with_context(system_prompt, user_message)
            return {
                "product_strategy": strategy,
                "status": "success",
            }
        except Exception as e:
            logger.error(f"Strategy development failed: {e}")
            return {"status": "error", "error": str(e)}

    def develop_gtm_strategy(
        self,
        product_name: str,
        target_customers: List[str],
        value_proposition: str,
        market_segment: str,
    ) -> Dict[str, Any]:
        """Develop go-to-market strategy."""
        system_prompt = """You are a go-to-market expert.
        Develop a comprehensive GTM strategy including:
        - Launch positioning and messaging
        - Target customer segments and buyer personas
        - Sales and distribution channels
        - Pricing strategy
        - Marketing and awareness plan
        - Sales enablement approach
        - Launch timeline and phases
        - Success metrics
        
        Be specific and actionable."""

        user_message = f"""Develop GTM strategy for:

Product: {product_name}

Target Customers: {', '.join(target_customers)}

Value Proposition: {value_proposition}

Market Segment: {market_segment}

Create a detailed GTM plan with messaging, channels, and timeline."""

        try:
            gtm = self.llm.generate_with_context(system_prompt, user_message)
            return {
                "gtm_strategy": gtm,
                "product": product_name,
                "status": "success",
            }
        except Exception as e:
            logger.error(f"GTM strategy development failed: {e}")
            return {"status": "error", "error": str(e)}

    def develop_pricing_strategy(
        self,
        product: str,
        competitors: List[str],
        value_prop: str,
        target_segment: str,
    ) -> Dict[str, Any]:
        """Develop pricing strategy."""
        system_prompt = """You are a pricing strategy expert.
        Develop a comprehensive pricing strategy that includes:
        - Pricing model (SaaS, perpetual, hybrid, etc.)
        - Tier structure and feature mapping
        - Price points and rationale
        - Competitive positioning
        - Packaging recommendations
        - Launch pricing and future adjustments
        - Revenue projections
        
        Consider value, competition, and target customer willingness to pay."""

        user_message = f"""Develop pricing strategy for:

Product: {product}

Competitors: {', '.join(competitors)}

Value Proposition: {value_prop}

Target: {target_segment}

Create a detailed pricing strategy with tiers and rationale."""

        try:
            pricing = self.llm.generate_with_context(system_prompt, user_message)
            return {
                "pricing_strategy": pricing,
                "product": product,
                "status": "success",
            }
        except Exception as e:
            logger.error(f"Pricing strategy development failed: {e}")
            return {"status": "error", "error": str(e)}

    def analyze_strategic_options(
        self, options: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """Analyze strategic options and recommend best path."""
        system_prompt = """You are a strategic advisor.
        Analyze the provided strategic options and:
        - Evaluate pros and cons of each
        - Assess strategic fit and alignment
        - Evaluate resource requirements
        - Assess risk and uncertainty
        - Estimate potential outcomes
        - Recommend the best option with rationale
        
        Be analytical and data-driven in your assessment."""

        options_str = "\n\n".join(
            [
                f"Option {i+1}: {opt.get('name', f'Option {i+1}')}\n{opt.get('description', '')}"
                for i, opt in enumerate(options)
            ]
        )

        user_message = f"""Analyze these strategic options:

{options_str}

Compare and recommend the best strategic path forward."""

        try:
            analysis = self.llm.generate_with_context(system_prompt, user_message)
            return {
                "options_analyzed": len(options),
                "analysis": analysis,
                "status": "success",
            }
        except Exception as e:
            logger.error(f"Strategic analysis failed: {e}")
            return {"status": "error", "error": str(e)}
