"""User research and customer insights module."""

import logging
from typing import Any, Dict, List
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from config.settings import settings

logger = logging.getLogger(__name__)


class UserResearchAnalyzer:
    """Analyzes user feedback, surveys, and research data."""

    def __init__(self, model: str = None):
        """Initialize the user research analyzer."""
        self.model_name = model or settings.DEFAULT_MODEL
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=self.model_name,
            temperature=0.7,
        )
        logger.info(f"Initialized UserResearchAnalyzer with model: {self.model_name}")

    def analyze_interviews(self, transcripts: List[str]) -> Dict[str, Any]:
        """Analyze interview transcripts to extract insights."""
        combined = "\n\n---INTERVIEW BREAK---\n\n".join(transcripts)
        
        prompt = PromptTemplate(
            input_variables=["transcripts"],
            template="""Analyze these user interview transcripts and extract:

1. Key Themes
   - Recurring topics
   - Pain points
   - Desired features
   - Workflow patterns

2. User Jobs
   - Primary jobs to be done
   - Supporting jobs
   - Emotional jobs

3. Pain Points (ranked by frequency)
   - Current solutions
   - Severity
   - Workarounds used

4. Desired Outcomes
   - Must-have features
   - Nice-to-have features
   - Success metrics

5. User Personas
   - Segments identified
   - Characteristics
   - Motivations

6. Actionable Insights
   - Immediate actions
   - Strategic implications
   - Validation needs

Transcripts:
{transcripts}

Provide response as JSON.""",
        )

        chain = prompt | self.llm
        response = chain.invoke({"transcripts": combined})
        
        try:
            result = json.loads(response.content)
        except json.JSONDecodeError:
            result = {"interviews": len(transcripts), "analysis": response.content}
        
        return result

    def analyze_surveys(self, survey_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze survey responses and aggregated data."""
        survey_str = json.dumps(survey_data, indent=2)
        
        prompt = PromptTemplate(
            input_variables=["survey"],
            template="""Analyze this survey data and provide:

1. Key Statistics
   - Response rate
   - Sample demographics
   - Key metrics

2. Response Patterns
   - Most common responses
   - Variations by segment
   - Outliers

3. Sentiment Analysis
   - Overall satisfaction
   - Sentiment by topic
   - Emotional indicators

4. Feature Requests (ranked)
   - Most requested features
   - Frequency analysis
   - User segment interest

5. Satisfaction Drivers
   - What matters most
   - Correlation analysis
   - Investment priorities

6. Recommendations
   - Strategic insights
   - Immediate improvements
   - Long-term direction

Survey Data:
{survey}

Provide response as JSON.""",
        )

        chain = prompt | self.llm
        response = chain.invoke({"survey": survey_str})
        
        try:
            result = json.loads(response.content)
        except json.JSONDecodeError:
            result = {"responses": len(survey_data), "analysis": response.content}
        
        return result

    def synthesize_research(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize multiple research sources into insights."""
        research_str = json.dumps(research_data, indent=2)
        
        prompt = PromptTemplate(
            input_variables=["research"],
            template="""Synthesize this research data into cohesive insights:

1. User Personas (3-5)
   - Name, role, background
   - Goals and motivations
   - Pain points and frustrations
   - Success criteria

2. Jobs to Be Done
   - Primary jobs
   - Context and triggers
   - Current solutions
   - Desired outcomes

3. Opportunity Areas
   - Unmet needs
   - Market opportunities
   - Priority ranking
   - Addressability assessment

4. Feature Priorities
   - Must-have features
   - High-value features
   - Engagement drivers
   - Retention factors

5. Go-to-Market Insights
   - Key messaging
   - Target segments
   - Acquisition channels
   - Competitive positioning

Research Data:
{research}

Provide response as JSON.""",
        )

        chain = prompt | self.llm
        response = chain.invoke({"research": research_str})
        
        try:
            result = json.loads(response.content)
        except json.JSONDecodeError:
            result = {"synthesis": response.content}
        
        return result
