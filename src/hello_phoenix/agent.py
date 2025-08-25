"""LangGraph agent for greeting in multiple languages."""

from typing import Annotated, Sequence, TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import sys
from pathlib import Path
# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools"))
from agent.greeting_tools import get_all_tools


class AgentState(TypedDict):
    """State for the greeting agent."""
    messages: Annotated[Sequence[BaseMessage], "Messages in the conversation"]


def create_greeting_agent(openai_api_key: str):
    """Create a LangGraph agent for greeting in multiple languages.
    
    Args:
        openai_api_key: OpenAI API key
        
    Returns:
        Compiled LangGraph workflow
    """
    tools = get_all_tools()
    
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        api_key=openai_api_key,
        temperature=0
    )
    
    llm_with_tools = llm.bind_tools(tools)
    
    system_prompt = SystemMessage(content="""You are a greeting assistant that can greet people in different languages.
You MUST use the appropriate tool for each language:
- Use hello_english for English greetings
- Use hello_mandarin for Mandarin/Chinese greetings  
- Use hello_spanish for Spanish greetings
- Use hello_hebrew for Hebrew greetings

IMPORTANT: You must ALWAYS use the tools to generate greetings. Never generate greetings yourself.""")
    
    def call_model(state: AgentState):
        """Call the LLM with tools."""
        messages = [system_prompt] + state["messages"]
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}
    
    def should_continue(state: AgentState):
        """Check if we should continue to tools or end."""
        last_message = state["messages"][-1]
        # If the last message has tool_calls, we need to execute them
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "continue"
        # Otherwise we're done
        return "end"
    
    tool_node = ToolNode(tools)
    
    workflow = StateGraph(AgentState)
    
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)
    
    workflow.set_entry_point("agent")
    
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "end": END
        }
    )
    
    workflow.add_edge("tools", END)
    
    return workflow.compile()