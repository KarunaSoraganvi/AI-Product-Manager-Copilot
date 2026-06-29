"""Tests for utility functions."""

import pytest
from src.utils.data_processor import DataProcessor
from src.utils.formatters import OutputFormatter


class TestDataProcessor:
    """Test suite for DataProcessor."""

    def test_parse_json_safely_valid(self):
        """Test parsing valid JSON."""
        result = DataProcessor.parse_json_safely('{"key": "value"}')
        assert result == {"key": "value"}

    def test_parse_json_safely_invalid(self):
        """Test parsing invalid JSON."""
        result = DataProcessor.parse_json_safely('{invalid json}')
        assert result == {}

    def test_clean_text(self):
        """Test text cleaning."""
        dirty_text = "  hello   world  "
        clean = DataProcessor.clean_text(dirty_text)
        assert clean == "hello world"

    def test_extract_sentences(self):
        """Test sentence extraction."""
        text = "This is sentence one. This is sentence two."
        sentences = DataProcessor.extract_sentences(text)
        assert len(sentences) >= 2

    def test_analyze_sentiment(self):
        """Test sentiment analysis."""
        positive_text = "This is amazing!"
        result = DataProcessor.analyze_sentiment(positive_text)
        assert "sentiment" in result
        assert "polarity" in result
        assert result["sentiment"] in ["positive", "negative", "neutral"]

    def test_aggregate_data(self):
        """Test data aggregation."""
        data = [{"category": "A", "value": 1}, {"category": "B", "value": 2}]
        result = DataProcessor.aggregate_data(data)
        assert result is not None
        assert isinstance(result, dict)


class TestOutputFormatter:
    """Test suite for OutputFormatter."""

    def test_format_json(self):
        """Test JSON formatting."""
        data = {"key": "value", "nested": {"inner": "data"}}
        result = OutputFormatter.format_json(data, pretty=True)
        assert isinstance(result, str)
        assert "key" in result
        assert "value" in result

    def test_format_markdown(self):
        """Test markdown formatting."""
        content = {"Section1": {"key": "value"}}
        result = OutputFormatter.format_markdown("Title", content)
        assert isinstance(result, str)
        assert "Title" in result
        assert "Section1" in result

    def test_format_table(self):
        """Test table formatting."""
        data = [
            {"name": "Item1", "value": 100},
            {"name": "Item2", "value": 200}
        ]
        result = OutputFormatter.format_table(data)
        assert isinstance(result, str)
        assert "Item1" in result
        assert "Item2" in result

    def test_format_report(self):
        """Test report formatting."""
        sections = {"Section1": "Content1", "Section2": "Content2"}
        result = OutputFormatter.format_report("Title", sections)
        assert isinstance(result, str)
        assert "Title" in result
        assert "Section1" in result
