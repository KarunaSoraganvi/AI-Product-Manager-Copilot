"""Output formatting utilities."""

import json
from typing import Any, Dict, List
from datetime import datetime


class OutputFormatter:
    """Formats analysis outputs."""

    @staticmethod
    def format_json(data: Dict[str, Any]) -> str:
        """Format data as JSON."""
        return json.dumps(data, indent=2, default=str)

    @staticmethod
    def format_markdown(title: str, content: Dict[str, Any]) -> str:
        """Format data as Markdown."""
        md = f"# {title}\n\n"
        for key, value in content.items():
            md += f"## {key.replace('_', ' ').title()}\n"
            if isinstance(value, list):
                for item in value:
                    md += f"- {item}\n"
            elif isinstance(value, dict):
                for k, v in value.items():
                    md += f"- **{k}**: {v}\n"
            else:
                md += f"{value}\n"
            md += "\n"
        return md

    @staticmethod
    def format_report(
        title: str,
        summary: str,
        sections: Dict[str, Any],
        metadata: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Format comprehensive report."""
        report = {
            "title": title,
            "generated_at": datetime.now().isoformat(),
            "summary": summary,
            "sections": sections,
        }
        if metadata:
            report["metadata"] = metadata
        return report

    @staticmethod
    def format_recommendations(
        recommendations: List[str],
        priorities: List[str] = None,
        next_steps: List[str] = None,
    ) -> Dict[str, Any]:
        """Format recommendations with priorities and next steps."""
        return {
            "recommendations": recommendations,
            "high_priority": priorities or [],
            "next_steps": next_steps or [],
            "count": len(recommendations),
        }

    @staticmethod
    def format_roadmap(
        phases: List[Dict[str, Any]], timeline: str = None
    ) -> Dict[str, Any]:
        """Format roadmap output."""
        return {
            "timeline": timeline or "TBD",
            "phases": phases,
            "total_phases": len(phases),
        }

    @staticmethod
    def format_error(error_code: str, message: str, details: str = None) -> Dict[str, Any]:
        """Format error response."""
        error_response = {
            "error": True,
            "code": error_code,
            "message": message,
        }
        if details:
            error_response["details"] = details
        return error_response
