"""User research and feedback analysis module."""

from typing import Dict, List, Any
import logging
from src.utils.llm_client import get_llm_client

logger = logging.getLogger(__name__)


class UserResearchAnalyzer:
    """Analyzes user feedback and research data."""

    def __init__(self):
        self.llm = get_llm_client()

    def synthesize_interviews(
        self, interviews: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """Synthesize findings from multiple user interviews."""
        system_prompt = """You are a user research analyst.
        Synthesize the following interview data to identify:
        - User pain points and needs
        - Common patterns and themes
        - Feature requests and preferences
        - Customer segments and personas
        - Opportunities for product improvement
        
        Provide actionable insights for product decisions."""

        interviews_str = "\n\n".join(
            [
                f"Interview {i+1}: {interview.get('participant', f'Participant {i+1}')}\n{interview.get('transcript', '')}"
                for i, interview in enumerate(interviews)
            ]
        )

        user_message = f"""Synthesize these user interviews:

{interviews_str}

Identify key themes, pain points, needs, and product opportunities."""

        try:
            synthesis = self.llm.generate_with_context(system_prompt, user_message)
            return {
                "interviews_analyzed": len(interviews),
                "synthesis": synthesis,
                "status": "success",
            }
        except Exception as e:
            logger.error(f"Interview synthesis failed: {e}")
            return {"status": "error", "error": str(e)}

    def analyze_feedback(self, feedback_items: List[str]) -> Dict[str, Any]:
        """Analyze and categorize user feedback."""
        system_prompt = """You are a feedback analyst.
        Analyze the provided feedback to:
        - Categorize by theme or topic
        - Identify sentiment (positive, negative, neutral)
        - Extract actionable insights
        - Identify feature requests vs bug reports
        - Assess priority and impact
        
        Provide structured analysis with recommendations."""

        feedback_str = "\n".join([f"- {item}" for item in feedback_items])

        user_message = f"""Analyze this user feedback:

{feedback_str}

Categorize, sentiment analyze, and provide actionable insights."""

        try:
            analysis = self.llm.generate_with_context(system_prompt, user_message)
            return {
                "feedback_items_analyzed": len(feedback_items),
                "analysis": analysis,
                "status": "success",
            }
        except Exception as e:
            logger.error(f"Feedback analysis failed: {e}")
            return {"status": "error", "error": str(e)}

    def identify_personas(
        self, user_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Identify user personas from research data."""
        system_prompt = """You are a user research specialist.
        Based on the provided user data, identify distinct user personas.
        For each persona, describe:
        - Demographics and background
        - Goals and motivations
        - Pain points and frustrations
        - Use cases and workflows
        - Needs and priorities
        
        Provide actionable persona descriptions for product decisions."""

        users_str = "\n".join(
            [
                f"User {i+1}: {u.get('description', str(u))}"
                for i, u in enumerate(user_data)
            ]
        )

        user_message = f"""Identify user personas from this data:

{users_str}

Define distinct personas with goals, pain points, and needs."""

        try:
            personas = self.llm.generate_with_context(system_prompt, user_message)
            return {
                "users_analyzed": len(user_data),
                "personas": personas,
                "status": "success",
            }
        except Exception as e:
            logger.error(f"Persona identification failed: {e}")
            return {"status": "error", "error": str(e)}

    def analyze_feature_requests(
        self, feature_requests: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """Analyze and prioritize feature requests from users."""
        system_prompt = """You are a product manager analyzing feature requests.
        Analyze the requests and provide:
        - Categorization and clustering
        - User demand estimation
        - Impact assessment
        - Implementation complexity
        - Strategic alignment
        - Prioritization recommendation
        
        Consider both volume and value of requests."""

        requests_str = "\n".join(
            [
                f"Request: {r.get('title', 'Untitled')} - {r.get('description', '')}"
                for r in feature_requests
            ]
        )

        user_message = f"""Analyze these feature requests:

{requests_str}

Categorize, prioritize, and recommend which to build."""

        try:
            analysis = self.llm.generate_with_context(system_prompt, user_message)
            return {
                "requests_analyzed": len(feature_requests),
                "analysis": analysis,
                "status": "success",
            }
        except Exception as e:
            logger.error(f"Feature request analysis failed: {e}")
            return {"status": "error", "error": str(e)}
