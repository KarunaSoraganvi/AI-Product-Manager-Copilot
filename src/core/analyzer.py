"""Core analysis engine for AI Product Manager Copilot."""

import logging
import json
from typing import Dict, List, Any
from src.utils.llm_client import get_llm_client

logger = logging.getLogger(__name__)


class AnalysisEngine:
    """Core engine for analyzing product management data."""

    def __init__(self):
        self.llm = get_llm_client()

    def analyze_text(self, text: str, analysis_type: str = "general") -> Dict[str, Any]:
        """Analyze text content."""
        prompts = {
            "general": "Analyze the following text and provide key insights:\n\n{text}",
            "sentiment": "Analyze the sentiment and emotional tone of: {text}",
            "summary": "Provide a concise summary of: {text}",
            "themes": "Identify main themes and patterns in: {text}",
        }

        prompt = prompts.get(analysis_type, prompts["general"]).format(text=text)

        try:
            result = self.llm.generate(prompt)
            return {
                "analysis_type": analysis_type,
                "result": result,
                "status": "success",
            }
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return {
                "analysis_type": analysis_type,
                "status": "error",
                "error": str(e),
            }

    def extract_insights(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract actionable insights from data."""
        system_prompt = """You are an expert product manager analyst. 
        Extract key insights, patterns, and actionable recommendations from the provided data.
        Focus on business impact and strategic importance."""

        user_message = f"Extract insights from this data:\n\n{str(data)}"

        try:
            insights = self.llm.generate_with_context(system_prompt, user_message)
            return {
                "insights": insights,
                "status": "success",
            }
        except Exception as e:
            logger.error(f"Insight extraction failed: {e}")
            return {
                "status": "error",
                "error": str(e),
            }

    def compare_items(
        self, items: List[Dict[str, Any]], comparison_criteria: List[str]
    ) -> Dict[str, Any]:
        """Compare multiple items across criteria."""
        system_prompt = """You are an expert analyst. 
        Compare the provided items across the specified criteria.
        Provide structured analysis with pros and cons for each."""

        user_message = f"""Compare these items:
        
{json.dumps(items, indent=2)}

Across these criteria: {', '.join(comparison_criteria)}"""

        try:
            comparison = self.llm.generate_with_context(system_prompt, user_message)
            return {
                "comparison": comparison,
                "items_compared": len(items),
                "criteria": comparison_criteria,
                "status": "success",
            }
        except Exception as e:
            logger.error(f"Comparison failed: {e}")
            return {
                "status": "error",
                "error": str(e),
            }

    def synthesize_data(self, data_points: List[str]) -> Dict[str, Any]:
        """Synthesize multiple data points into coherent insights."""
        system_prompt = """You are an expert at synthesizing diverse data points.
        Create a coherent narrative that connects the provided information.
        Identify patterns, correlations, and key takeaways."""

        user_message = f"""Synthesize these data points:

{chr(10).join(f'- {point}' for point in data_points)}"""

        try:
            synthesis = self.llm.generate_with_context(system_prompt, user_message)
            return {
                "synthesis": synthesis,
                "data_points_analyzed": len(data_points),
                "status": "success",
            }
        except Exception as e:
            logger.error(f"Synthesis failed: {e}")
            return {
                "status": "error",
                "error": str(e),
            }
