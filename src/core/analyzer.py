"""Core data analysis engine for the AI Product Manager Copilot."""

import logging
from typing import Any, Dict, List
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from config.settings import settings

logger = logging.getLogger(__name__)


class DataAnalyzer:
    """Analyzes product and market data using LLM."""

    def __init__(self, model: str = None):
        """Initialize the analyzer with an LLM."""
        self.model_name = model or settings.DEFAULT_MODEL
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=self.model_name,
            temperature=0.7,
        )
        logger.info(f"Initialized DataAnalyzer with model: {self.model_name}")

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text data."""
        prompt = PromptTemplate(
            input_variables=["text"],
            template="""Analyze the sentiment of the following text. Provide:
1. Overall sentiment (positive, negative, neutral)
2. Confidence score (0-1)
3. Key emotional indicators
4. Actionable insights

Text: {text}

Provide response as JSON.""",
        )

        chain = prompt | self.llm
        response = chain.invoke({"text": text})
        
        try:
            result = json.loads(response.content)
        except json.JSONDecodeError:
            result = {"sentiment": "neutral", "confidence": 0.5, "text": response.content}
        
        return result

    def extract_key_themes(self, data: List[str]) -> Dict[str, Any]:
        """Extract key themes from multiple data points."""
        combined_text = "\n".join(data)
        
        prompt = PromptTemplate(
            input_variables=["data"],
            template="""Analyze the following data points and extract:
1. Top 5 recurring themes
2. Patterns and correlations
3. Outliers or unique insights
4. Confidence level for each theme

Data:
{data}

Provide response as JSON.""",
        )

        chain = prompt | self.llm
        response = chain.invoke({"data": combined_text})
        
        try:
            result = json.loads(response.content)
        except json.JSONDecodeError:
            result = {"themes": [], "analysis": response.content}
        
        return result

    def synthesize_insights(self, analysis_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Synthesize multiple analysis results into actionable insights."""
        combined_analysis = json.dumps(analysis_results, indent=2)
        
        prompt = PromptTemplate(
            input_variables=["analysis"],
            template="""Based on the following analysis results, synthesize into:
1. Key strategic insights
2. Product recommendations
3. Risk factors
4. Opportunities
5. Priority actions

Analysis Results:
{analysis}

Provide response as JSON.""",
        )

        chain = prompt | self.llm
        response = chain.invoke({"analysis": combined_analysis})
        
        try:
            result = json.loads(response.content)
        except json.JSONDecodeError:
            result = {"insights": response.content}
        
        return result
