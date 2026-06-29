"""Data processing utilities."""

import logging
from typing import Any, Dict, List
import json
import pandas as pd
from nltk.tokenize import sent_tokenize
from textblob import TextBlob

logger = logging.getLogger(__name__)


class DataProcessor:
    """Utilities for processing and cleaning data."""

    @staticmethod
    def parse_json_safely(text: str) -> Dict[str, Any]:
        """Parse JSON text safely, returning empty dict on failure."""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON")
            return {}

    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text."""
        text = text.strip()
        text = " ".join(text.split())  # Remove extra whitespace
        return text

    @staticmethod
    def extract_sentences(text: str) -> List[str]:
        """Extract sentences from text."""
        return sent_tokenize(text)

    @staticmethod
    def analyze_sentiment(text: str) -> Dict[str, Any]:
        """Analyze sentiment of text using TextBlob."""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        return {
            "sentiment": sentiment,
            "polarity": round(polarity, 3),
            "subjectivity": round(subjectivity, 3),
        }

    @staticmethod
    def aggregate_data(data_list: List[Dict[str, Any]], groupby: str = None) -> Dict[str, Any]:
        """Aggregate list of data dictionaries."""
        df = pd.DataFrame(data_list)
        
        if groupby and groupby in df.columns:
            grouped = df.groupby(groupby).size().to_dict()
            return grouped
        
        # Return basic stats
        return {
            "count": len(df),
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.to_dict(),
        }

    @staticmethod
    def format_for_llm(data: Dict[str, Any]) -> str:
        """Format data for LLM input."""
        return json.dumps(data, indent=2)
