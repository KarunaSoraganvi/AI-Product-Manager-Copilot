"""Output formatting utilities."""

import json
from typing import Any, Dict, List
from datetime import datetime


class OutputFormatter:
    """Utilities for formatting output for users."""

    @staticmethod
    def format_json(data: Dict[str, Any], pretty: bool = True) -> str:
        """Format data as JSON."""
        return json.dumps(data, indent=2 if pretty else None)

    @staticmethod
    def format_markdown(title: str, content: Dict[str, Any]) -> str:
        """Format output as markdown."""
        lines = [f"# {title}\n"]
        lines.append(f"*Generated: {datetime.now().isoformat()}*\n")
        
        for section, data in content.items():
            lines.append(f"## {section}\n")
            if isinstance(data, dict):
                for key, value in data.items():
                    lines.append(f"- **{key}**: {value}")
            elif isinstance(data, list):
                for item in data:
                    lines.append(f"- {item}")
            else:
                lines.append(str(data))
            lines.append("")
        
        return "\n".join(lines)

    @staticmethod
    def format_table(data: List[Dict[str, Any]]) -> str:
        """Format data as markdown table."""
        if not data:
            return "No data to display"
        
        keys = data[0].keys()
        lines = []
        
        # Header
        lines.append("| " + " | ".join(str(k) for k in keys) + " |")
        lines.append("|" + "|" .join([" --- " for _ in keys]) + "|")
        
        # Rows
        for row in data:
            lines.append("| " + " | ".join(str(row.get(k, "")) for k in keys) + " |")
        
        return "\n".join(lines)

    @staticmethod
    def format_report(title: str, sections: Dict[str, Any]) -> str:
        """Format comprehensive report."""
        output = f"\n{'='*80}\n"
        output += f"{title.upper()}".center(80) + "\n"
        output += f"{'='*80}\n\n"
        
        for section_title, section_content in sections.items():
            output += f"\n{section_title}\n"
            output += "-" * len(section_title) + "\n"
            
            if isinstance(section_content, dict):
                for key, value in section_content.items():
                    output += f"{key}: {value}\n"
            elif isinstance(section_content, list):
                for item in section_content:
                    output += f"  • {item}\n"
            else:
                output += f"{section_content}\n"
        
        return output
