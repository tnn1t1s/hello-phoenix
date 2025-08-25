#!/usr/bin/env python3
import os
import time
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from src.hello_phoenix.tracing import setup_tracing
from src.hello_phoenix.agent import create_greeting_agent

# Load configuration from .env file
load_dotenv()

def main():
    # Setup tracing
    setup_tracing()
    
    # Create the greeting agent
    agent = create_greeting_agent(os.getenv("OPENAI_API_KEY"))
    
    print("🚀 Hello Phoenix - Multi-Agent Greeter")
    print("-" * 50)
    
    # Test different language greetings
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
        
        # Get the tool response
        for msg in result["messages"]:
            if hasattr(msg, "content") and msg.content:
                if "Hello" in msg.content or "Hola" in msg.content or "你好" in msg.content or "שלום" in msg.content:
                    print(f"   Result: {msg.content}")
    
    # Give time for traces to be sent
    print("\n⏳ Waiting for traces to be sent...")
    time.sleep(2)
    
    print(f"\n📈 View traces at: {os.getenv('PHOENIX_HOST')}")
    print("📊 Go to Projects → hello-phoenix to see all tool calls traced")

if __name__ == "__main__":
    main()
