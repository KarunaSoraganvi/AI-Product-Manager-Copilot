"""Product analytics and metrics interpretation module."""

from typing import Dict, List, Any
import logging
from src.utils.llm_client import get_llm_client

logger = logging.getLogger(__name__)


class AnalyticsInterpreter:
    """Interprets product metrics and analytics."""

    def __init__(self):
        self.llm = get_llm_client()

    def interpret_metrics(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Interpret product metrics and KPIs."""
        system_prompt = """You are a data analyst and product expert.
        Interpret the provided metrics to:
        - Identify key trends and patterns
        - Assess product health
        - Highlight areas of concern or opportunity
        - Provide actionable insights
        - Recommend improvements or next steps
        - Put metrics in context of business goals
        
        Be specific and data-driven."""

        metrics_str = "\n".join(
            [f"- {k}: {v}" for k, v in metrics.items()]
        )

        user_message = f"""Interpret these product metrics:

{metrics_str}

What do these metrics tell us about product health and performance?
What should we do about it?"""

        try:
            interpretation = self.llm.generate_with_context(
                system_prompt, user_message
            )
            return {
                "metrics_interpreted": len(metrics),
                "interpretation": interpretation,
                "status": "success",
            }
        except Exception as e:
            logger.error(f"Metrics interpretation failed: {e}")
            return {"status": "error", "error": str(e)}

    def analyze_user_cohorts(
        self, cohorts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze user cohort data."""
        system_prompt = """You are a cohort analysis expert.
        Analyze the provided user cohorts to identify:
        - Behavioral patterns between cohorts
        - Retention and engagement differences
        - Churn risks and opportunities
        - Feature adoption rates
        - Segment-specific insights
        - Recommendations for each cohort
        
        Focus on actionable insights."""

        cohorts_str = "\n\n".join(
            [
                f"Cohort {i+1}: {c.get('name', f'Cohort {i+1}')}\n{str(c)}"
                for i, c in enumerate(cohorts)
            ]
        )

        user_message = f"""Analyze these user cohorts:

{cohorts_str}

What patterns emerge? What should we do for each cohort?"""

        try:
            analysis = self.llm.generate_with_context(system_prompt, user_message)
            return {
                "cohorts_analyzed": len(cohorts),
                "analysis": analysis,
                "status": "success",
            }
        except Exception as e:
            logger.error(f"Cohort analysis failed: {e}")
            return {"status": "error", "error": str(e)}

    def predict_trends(
        self, historical_data: List[Dict[str, Any]], metric_name: str
    ) -> Dict[str, Any]:
        """Predict future trends based on historical data."""
        system_prompt = """You are a data analyst with forecasting expertise.
        Based on historical data, predict future trends for the metric.
        Include:
        - Trend direction and magnitude
        - Key drivers of the trend
        - Potential inflection points
        - Confidence level in the prediction
        - Scenarios for different conditions
        - Recommendations based on predictions
        
        Be balanced and acknowledge uncertainty."""

        data_str = "\n".join(
            [
                f"Period {i+1}: {d.get('period', f'Period {i+1}')} - Value: {d.get('value', 'N/A')}"
                for i, d in enumerate(historical_data)
            ]
        )

        user_message = f"""Predict future trends for {metric_name}:

Historical Data:
{data_str}

What's the trend? Where is it heading? What should we prepare for?"""

        try:
            prediction = self.llm.generate_with_context(system_prompt, user_message)
            return {
                "metric": metric_name,
                "data_points": len(historical_data),
                "prediction": prediction,
                "status": "success",
            }
        except Exception as e:
            logger.error(f"Trend prediction failed: {e}")
            return {"status": "error", "error": str(e)}

    def benchmark_performance(
        self, your_metrics: Dict[str, Any], industry_benchmarks: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare performance against industry benchmarks."""
        system_prompt = """You are a benchmarking analyst.
        Compare your product's metrics against industry benchmarks to:
        - Identify areas of strength
        - Highlight underperforming areas
        - Assess competitive positioning
        - Identify improvement opportunities
        - Provide context on industry trends
        - Recommend focus areas for improvement
        
        Be balanced and specific."""

        your_metrics_str = "\n".join(
            [f"- {k}: {v}" for k, v in your_metrics.items()]
        )
        benchmarks_str = "\n".join(
            [f"- {k}: {v}" for k, v in industry_benchmarks.items()]
        )

        user_message = f"""Compare our performance to industry benchmarks:

Our Metrics:
{your_metrics_str}

Industry Benchmarks:
{benchmarks_str}

How do we compare? Where should we focus?"""

        try:
            benchmark = self.llm.generate_with_context(system_prompt, user_message)
            return {
                "your_metrics_count": len(your_metrics),
                "benchmarks_count": len(industry_benchmarks),
                "comparison": benchmark,
                "status": "success",
            }
        except Exception as e:
            logger.error(f"Benchmarking failed: {e}")
            return {"status": "error", "error": str(e)}
