"""Analytics and metrics interpretation module."""

import logging
from typing import Any, Dict, List
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from config.settings import settings

logger = logging.getLogger(__name__)


class AnalyticsInterpreter:
    """Interprets metrics and KPIs to drive product decisions."""

    def __init__(self, model: str = None):
        """Initialize the analytics interpreter."""
        self.model_name = model or settings.DEFAULT_MODEL
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=self.model_name,
            temperature=0.6,
        )
        logger.info(f"Initialized AnalyticsInterpreter with model: {self.model_name}")

    def interpret_metrics(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Interpret product metrics and provide insights."""
        metrics_str = json.dumps(metrics, indent=2)
        
        prompt = PromptTemplate(
            input_variables=["metrics"],
            template="""Interpret these product metrics and provide analysis:

1. Health Assessment
   - Overall product health score
   - Trend direction
   - Red flags or concerns

2. Key Insights
   - What metrics tell us
   - Changes vs baseline
   - Anomalies and patterns

3. User Behavior Analysis
   - Engagement patterns
   - Retention trends
   - Churn indicators
   - Feature adoption

4. Performance Assessment
   - Strength areas
   - Weakness areas
   - Benchmarking vs industry
   - Competitive positioning

5. Actionable Recommendations
   - Immediate actions
   - Experimentation ideas
   - Strategic initiatives
   - Priority fixes

6. Forecast & Projections
   - 3-month forecast
   - Trend extrapolation
   - Risk scenarios

Metrics:
{metrics}

Provide response as JSON.""",
        )

        chain = prompt | self.llm
        response = chain.invoke({"metrics": metrics_str})
        
        try:
            result = json.loads(response.content)
        except json.JSONDecodeError:
            result = {"metrics_count": len(metrics), "analysis": response.content}
        
        return result

    def analyze_cohort(self, cohort_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user cohort behavior and retention."""
        cohort_str = json.dumps(cohort_data, indent=2)
        
        prompt = PromptTemplate(
            input_variables=["cohort"],
            template="""Analyze this cohort retention data:

1. Cohort Performance
   - Retention curves by cohort
   - Best/worst performing cohorts
   - Cohort size trends

2. Retention Insights
   - Week 1 retention (stickiness)
   - Long-term retention trends
   - Drop-off patterns
   - Seasonality effects

3. Segment Analysis
   - Performance by segment
   - Segmentation opportunities
   - High-value cohorts

4. Improvement Opportunities
   - Onboarding improvements
   - Engagement drivers
   - Churn prevention
   - Monetization levers

5. Experiment Recommendations
   - A/B test ideas
   - Measurement approach
   - Expected impact

Cohort Data:
{cohort}

Provide response as JSON.""",
        )

        chain = prompt | self.llm
        response = chain.invoke({"cohort": cohort_str})
        
        try:
            result = json.loads(response.content)
        except json.JSONDecodeError:
            result = {"cohort_analysis": response.content}
        
        return result

    def forecast_trends(self, historical_data: Dict[str, List[float]], metrics: List[str] = None) -> Dict[str, Any]:
        """Forecast future trends based on historical data."""
        metrics = metrics or []
        data_str = json.dumps(historical_data, indent=2)
        
        prompt = PromptTemplate(
            input_variables=["data", "metrics"],
            template="""Based on this historical data, forecast trends:

1. Trend Analysis
   - Current trend direction
   - Trend strength
   - Seasonality patterns
   - Growth acceleration/deceleration

2. Forecasts (3, 6, 12 months)
   - Projected values
   - Confidence intervals
   - Best/worst case scenarios

3. Inflection Points
   - Expected changes
   - Critical thresholds
   - Trigger events

4. Risk Factors
   - External dependencies
   - Market risks
   - Execution risks

5. Opportunity Windows
   - Optimal timing for initiatives
   - Resource allocation timing
   - Market windows

Historical Data:
{data}

Key Metrics: {metrics}

Provide response as JSON.""",
        )

        chain = prompt | self.llm
        response = chain.invoke({"data": data_str, "metrics": ", ".join(metrics) if metrics else "various"})
        
        try:
            result = json.loads(response.content)
        except json.JSONDecodeError:
            result = {"forecast": response.content}
        
        return result
