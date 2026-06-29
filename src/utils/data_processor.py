"""Data processing utilities for the copilot."""

import json
import logging
from typing import Any, Dict, List, Union
import pandas as pd

logger = logging.getLogger(__name__)


class DataProcessor:
    """Handles data processing and formatting."""

    @staticmethod
    def parse_json(data: Union[str, Dict]) -> Dict[str, Any]:
        """Parse JSON string or return dict as-is."""
        if isinstance(data, str):
            try:
                return json.loads(data)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON: {e}")
                raise
        return data

    @staticmethod
    def parse_csv(csv_content: str) -> List[Dict[str, Any]]:
        """Parse CSV content into list of dicts."""
        try:
            df = pd.read_csv(pd.io.common.StringIO(csv_content))
            return df.to_dict(orient="records")
        except Exception as e:
            logger.error(f"CSV parsing error: {e}")
            raise

    @staticmethod
    def extract_text_blocks(text: str, delimiter: str = "\n\n") -> List[str]:
        """Extract text blocks separated by delimiter."""
        return [block.strip() for block in text.split(delimiter) if block.strip()]

    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text."""
        # Remove extra whitespace
        text = " ".join(text.split())
        return text.strip()

    @staticmethod
    def aggregate_feedback(feedback_list: List[str]) -> Dict[str, Any]:
        """Aggregate and categorize feedback items."""
        return {
            "total_items": len(feedback_list),
            "items": feedback_list,
            "cleaned_items": [DataProcessor.clean_text(item) for item in feedback_list],
        }

    @staticmethod
    def structure_market_data(
        competitors: List[str],
        market_size: str = None,
        growth_rate: str = None,
        trends: List[str] = None,
    ) -> Dict[str, Any]:
        """Structure market data for analysis."""
        return {
            "competitors": competitors,
            "market_size": market_size,
            "growth_rate": growth_rate,
            "trends": trends or [],
        }

    @staticmethod
    def score_features(
        features: List[Dict[str, Any]], scores: List[float]
    ) -> List[Dict[str, Any]]:
        """Add scores to features and sort by score."""
        scored_features = [
            {**feature, "score": score}
            for feature, score in zip(features, scores)
        ]
        return sorted(scored_features, key=lambda x: x["score"], reverse=True)
