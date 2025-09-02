#!/usr/bin/env python3
"""Single-call greeter - Makes 1 LLM call that invokes all 4 tools."""

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
    """Run the single-call greeter demo."""
    # Setup tracing with specific project name
    setup_tracing(project_name="single-call-greeter")
    # Create the greeting agent
    agent = create_greeting_agent(os.getenv("OPENAI_API_KEY"))
    print("🚀 Single-Call Greeter - 1 LLM Call Demo")
    print("-" * 50)
    # Single prompt asking for all 4 greetings at once
    combined_prompt = """Please greet the following people in their respective languages:
    1. Alice in English
    2. Bob in Spanish  
    3. Chen in Mandarin
    4. David in Hebrew
    
    Use the appropriate greeting tool for each person."""
    print("\n📝 Combined Prompt:")
    print(combined_prompt)
    print("\n" + "-" * 50)
    # Make a single agent invocation
    state = {"messages": [HumanMessage(content=combined_prompt)]}
    result = agent.invoke(state)
    # Print all responses
    print("\n🌍 Greetings Generated:")
    for msg in result["messages"]:
        if hasattr(msg, "content") and msg.content:
            # Skip the initial AI message planning the tool calls
            if not msg.content.startswith("I'll") and not msg.content.startswith(
                "I will"
            ):
                print(f"   • {msg.content}")
    # Give time for traces to be sent
    print("\n⏳ Waiting for traces to be sent...")
    time.sleep(2)
    print(f"\n📈 View traces at: {os.getenv('PHOENIX_HOST', 'http://localhost:6006')}")
    print("📊 Go to Projects → single-call-greeter to see 1 LLM call and 4 tool calls")


if __name__ == "__main__":
    main()
