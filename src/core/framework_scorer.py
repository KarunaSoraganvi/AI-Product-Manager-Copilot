"""Prioritization framework scorer for feature ranking."""

from typing import Dict, List, Any
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class FrameworkType(str, Enum):
    """Supported prioritization frameworks."""

    RICE = "RICE"
    MOSCOW = "MoSCoW"
    KANO = "Kano"
    VALUE_EFFORT = "ValueEffort"


class FeatureScorer:
    """Scores and ranks features using various frameworks."""

    @staticmethod
    def score_rice(
        features: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Score features using RICE framework.
        
        RICE = Reach * Impact * Confidence / Effort
        """
        scored = []
        for feature in features:
            reach = feature.get("reach", 1)
            impact = feature.get("impact", 1)  # 1=minimal, 2=minor, 3=normal, 4=major
            confidence = feature.get("confidence", 100) / 100
            effort = feature.get("effort", 1)  # in person-months

            score = (reach * impact * confidence) / max(effort, 0.5)

            scored.append({**feature, "rice_score": score})

        return sorted(scored, key=lambda x: x["rice_score"], reverse=True)

    @staticmethod
    def score_moscow(
        features: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Categorize features using MoSCoW method.
        
        Categories: Must, Should, Could, Won't
        """
        priority_map = {"Must": 4, "Should": 3, "Could": 2, "Won't": 1}

        scored = []
        for feature in features:
            priority = feature.get("moscow_priority", "Could")
            score = priority_map.get(priority, 0)

            scored.append({**feature, "moscow_score": score, "category": priority})

        return sorted(scored, key=lambda x: x["moscow_score"], reverse=True)

    @staticmethod
    def score_kano(features: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Score features using Kano model.
        
        Categories: Attractive, Performance, Basic
        """
        category_scores = {
            "Attractive": 3,
            "Performance": 2,
            "Basic": 1,
        }

        scored = []
        for feature in features:
            category = feature.get("kano_category", "Performance")
            score = category_scores.get(category, 0)

            scored.append({**feature, "kano_score": score, "category": category})

        return sorted(scored, key=lambda x: x["kano_score"], reverse=True)

    @staticmethod
    def score_value_effort(
        features: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Score using Value vs Effort matrix.
        
        Score = Value / Effort
        """
        scored = []
        for feature in features:
            value = feature.get("value", 1)
            effort = feature.get("effort", 1)

            score = value / max(effort, 0.1)
            quadrant = FeatureScorer._get_quadrant(value, effort)

            scored.append(
                {**feature, "value_effort_score": score, "quadrant": quadrant}
            )

        return sorted(scored, key=lambda x: x["value_effort_score"], reverse=True)

    @staticmethod
    def _get_quadrant(value: float, effort: float) -> str:
        """Determine which quadrant the feature falls into."""
        if value > 5 and effort <= 5:
            return "Quick Wins"
        elif value > 5 and effort > 5:
            return "Major Projects"
        elif value <= 5 and effort <= 5:
            return "Fill Ins"
        else:
            return "Time Sinks"

    @staticmethod
    def score_by_framework(
        features: List[Dict[str, Any]], framework: str = "RICE"
    ) -> List[Dict[str, Any]]:
        """Score features using specified framework."""
        framework_type = FrameworkType(framework)

        if framework_type == FrameworkType.RICE:
            return FeatureScorer.score_rice(features)
        elif framework_type == FrameworkType.MOSCOW:
            return FeatureScorer.score_moscow(features)
        elif framework_type == FrameworkType.KANO:
            return FeatureScorer.score_kano(features)
        elif framework_type == FrameworkType.VALUE_EFFORT:
            return FeatureScorer.score_value_effort(features)
        else:
            logger.warning(f"Unknown framework: {framework}, using RICE")
            return FeatureScorer.score_rice(features)

    @staticmethod
    def multi_framework_score(
        features: List[Dict[str, Any]],
        frameworks: List[str] = None,
    ) -> List[Dict[str, Any]]:
        """Score using multiple frameworks and combine results."""
        if frameworks is None:
            frameworks = ["RICE", "MOSCOW", "VALUE_EFFORT"]

        results = []
        for feature in features:
            combined_feature = feature.copy()

            for framework in frameworks:
                scored = FeatureScorer.score_by_framework([feature], framework)
                if scored:
                    for key, value in scored[0].items():
                        if key not in combined_feature and key != "name":
                            combined_feature[key] = value

            results.append(combined_feature)

        return results
