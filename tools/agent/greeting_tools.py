"""Greeting tools for different languages."""

from langchain_core.tools import tool


@tool
def hello_english(name: str) -> str:
    """Greet someone in English.
    
    Args:
        name: The person's name to greet
        
    Returns:
        Greeting in English
    """
    return f"Hello {name}"


@tool
def hello_mandarin(name: str) -> str:
    """Greet someone in Mandarin Chinese.
    
    Args:
        name: The person's name to greet
        
    Returns:
        Greeting in Mandarin (你好)
    """
    return f"你好 {name}"


@tool  
def hello_spanish(name: str) -> str:
    """Greet someone in Spanish.
    
    Args:
        name: The person's name to greet
        
    Returns:
        Greeting in Spanish
    """
    return f"Hola {name}"


@tool
def hello_hebrew(name: str) -> str:
    """Greet someone in Hebrew.
    
    Args:
        name: The person's name to greet
        
    Returns:
        Greeting in Hebrew (שלום)
    """
    return f"שלום {name}"


def get_all_tools():
    """Get all greeting tools as a list."""
    return [
        hello_english,
        hello_mandarin,
        hello_spanish,
        hello_hebrew
    ]