"""Tests for greeting tools."""

import pytest
from src.hello_phoenix.tools import (
    hello_english,
    hello_mandarin,
    hello_spanish,
    hello_hebrew,
    get_all_tools
)


class TestGreetingTools:
    """Test suite for greeting tools."""
    
    def test_hello_english(self):
        """Test English greeting."""
        result = hello_english.invoke({"name": "Alice"})
        assert result == "Hello Alice"
        
    def test_hello_mandarin(self):
        """Test Mandarin greeting."""
        result = hello_mandarin.invoke({"name": "Bob"})
        assert result == "你好 Bob"
        
    def test_hello_spanish(self):
        """Test Spanish greeting."""
        result = hello_spanish.invoke({"name": "Carlos"})
        assert result == "Hola Carlos"
        
    def test_hello_hebrew(self):
        """Test Hebrew greeting."""
        result = hello_hebrew.invoke({"name": "David"})
        assert result == "שלום David"
        
    def test_empty_name(self):
        """Test with empty name."""
        result = hello_english.invoke({"name": ""})
        assert result == "Hello "
        
    def test_special_characters(self):
        """Test with special characters in name."""
        result = hello_english.invoke({"name": "O'Brien"})
        assert result == "Hello O'Brien"
        
    def test_unicode_name(self):
        """Test with Unicode characters in name."""
        result = hello_spanish.invoke({"name": "José"})
        assert result == "Hola José"
        
    def test_get_all_tools(self):
        """Test getting all tools."""
        tools = get_all_tools()
        assert len(tools) == 4
        assert hello_english in tools
        assert hello_mandarin in tools
        assert hello_spanish in tools
        assert hello_hebrew in tools