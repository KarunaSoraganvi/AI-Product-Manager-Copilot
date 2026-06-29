"""Product strategy development module."""

import logging
from typing import Any, Dict, List
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from config.settings import settings

logger = logging.getLogger(__name__)


class StrategyDeveloper:
    """Develops comprehensive product strategies."""

    def __init__(self, model: str = None):
        """Initialize the strategy developer."""
        self.model_name = model or settings.DEFAULT_MODEL
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=self.model_name,
            temperature=0.7,
        )
        logger.info(f"Initialized StrategyDeveloper with model: {self.model_name}")

    def develop_strategy(self, context: Dict[str, Any], objectives: List[str]) -> Dict[str, Any]:
        """Develop comprehensive product strategy."""
        context_str = json.dumps(context, indent=2)
        objectives_str = "\n".join([f"- {obj}" for obj in objectives])
        
        prompt = PromptTemplate(
            input_variables=["context", "objectives"],
            template="""Develop a comprehensive product strategy:

Context:
{context}

Strategic Objectives:
{objectives}

Provide a strategy including:

1. Vision & Mission
   - 3-5 year vision
   - Mission statement
   - Core values

2. Strategic Pillars
   - 3-5 key pillars
   - Supporting initiatives
   - Success metrics

3. Market Positioning
   - Target market definition
   - Unique value proposition
   - Competitive advantage
   - Brand positioning

4. Go-to-Market Strategy
   - Launch approach
   - Customer acquisition
   - Pricing strategy
   - Distribution strategy

5. Growth Strategy
   - Market expansion
   - Product expansion
   - Partnership strategy
   - Monetization strategy

6. Organizational Strategy
   - Team structure
   - Capability building
   - Culture elements
   - Capability roadmap

7. Success Metrics
   - Key metrics
   - Quarterly targets
   - Leading indicators
   - Lagging indicators

Provide response as JSON.""",
        )

        chain = prompt | self.llm
        response = chain.invoke({"context": context_str, "objectives": objectives_str})
        
        try:
            result = json.loads(response.content)
        except json.JSONDecodeError:
            result = {"strategy": response.content}
        
        return result

    def gtm_planning(self, product_info: Dict[str, Any], market_info: Dict[str, Any]) -> Dict[str, Any]:
        """Plan go-to-market strategy."""
        product_str = json.dumps(product_info, indent=2)
        market_str = json.dumps(market_info, indent=2)
        
        prompt = PromptTemplate(
            input_variables=["product", "market"],
            template="""Develop a go-to-market strategy:

Product Information:
{product}

Market Information:
{market}

Provide GTM strategy including:

1. Target Customer Definition
   - Personas
   - Use cases
   - Customer segments
   - TAM/SAM/SOM

2. Positioning Strategy
   - Unique value proposition
   - Key messaging
   - Competitive positioning
   - Brand identity

3. Pricing Strategy
   - Pricing model
   - Price points
   - Packaging tiers
   - Discounting strategy

4. Sales Strategy
   - Sales model (direct/indirect)
   - Sales process
   - Channel strategy
   - Sales enablement

5. Marketing Strategy
   - Awareness tactics
   - Engagement tactics
   - Campaign calendar
   - Content strategy

6. Launch Plan
   - Timeline
   - Launch activities
   - Success metrics
   - Risk mitigation

7. Metrics & KPIs
   - Acquisition metrics
   - Conversion metrics
   - Retention metrics
   - Targets and goals

Provide response as JSON.""",
        )

        chain = prompt | self.llm
        response = chain.invoke({"product": product_str, "market": market_str})
        
        try:
            result = json.loads(response.content)
        except json.JSONDecodeError:
            result = {"gtm_plan": response.content}
        
        return result

    def stakeholder_alignment(self, strategy: Dict[str, Any], stakeholders: List[Dict[str, str]]) -> Dict[str, Any]:
        """Create stakeholder alignment documentation."""
        strategy_str = json.dumps(strategy, indent=2)
        stakeholders_str = json.dumps(stakeholders, indent=2)
        
        prompt = PromptTemplate(
            input_variables=["strategy", "stakeholders"],
            template="""Create stakeholder alignment for this strategy:

Strategy:
{strategy}

Stakeholders:
{stakeholders}

For each stakeholder group provide:
1. Key interests and priorities
2. Benefits of the strategy
3. Concerns or risks
4. Required commitments
5. Success metrics relevant to them
6. Communication approach

Also provide:
- Consensus points
- Areas of potential conflict
- Mitigation strategies
- Governance model
- Decision-making process
- Escalation path

Provide response as JSON.""",
        )

        chain = prompt | self.llm
        response = chain.invoke({"strategy": strategy_str, "stakeholders": stakeholders_str})
        
        try:
            result = json.loads(response.content)
        except json.JSONDecodeError:
            result = {"alignment": response.content}
        
        return result
