#!/usr/bin/env python3
"""Multi-call greeter - Makes 4 separate LLM calls (one per language)."""

import os
import sys
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# pylint: disable=wrong-import-position,import-error
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from src.hello_phoenix.tracing import setup_tracing
from src.hello_phoenix.agent import create_greeting_agent
# pylint: enable=wrong-import-position,import-error

# Load configuration from .env file
load_dotenv()


def main():
    """Run the multi-call greeter demo."""
    # Setup tracing with specific project name
    setup_tracing(project_name="multi-call-greeter")
    # Create the greeting agent
    agent = create_greeting_agent(os.getenv("OPENAI_API_KEY"))
    print("🚀 Multi-Call Greeter - 4 LLM Calls Demo")
    print("-" * 50)
    # Test different language greetings - each will be a separate LLM call
    test_cases = [
        ("Say hello to Alice in English", "English"),
        ("Greet Bob in Spanish", "Spanish"),
        ("Say hello to Chen in Mandarin", "Mandarin"),
        ("Greet David in Hebrew", "Hebrew"),
    ]
    for prompt, language in test_cases:
        print(f"\n🌍 {language} greeting:")
        print(f"   Prompt: {prompt}")
        state = {"messages": [HumanMessage(content=prompt)]}
        result = agent.invoke(state)
        # Print all messages without any filtering or heuristics
        for msg in result["messages"]:
            if hasattr(msg, "content") and msg.content:
                print(f"   Result: {msg.content}")
    # Give time for traces to be sent
    print("\n⏳ Waiting for traces to be sent...")
    time.sleep(2)
    print(f"\n📈 View traces at: {os.getenv('PHOENIX_HOST', 'http://localhost:6006')}")
    print("📊 Go to Projects → multi-call-greeter to see 4 LLM calls and 4 tool calls")


if __name__ == "__main__":
    main()
