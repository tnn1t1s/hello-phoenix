"""Hello Phoenix - Multi-agent greeting system with tracing."""

__version__ = "0.1.0"

from .agent import create_greeting_agent
from .tracing import setup_tracing

__all__ = [
    "create_greeting_agent",
    "setup_tracing",
]