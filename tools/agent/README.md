# Agent Tools

## Overview

This directory contains tools used by LangGraph agents for executing specific actions within workflows. Unlike the Phoenix management tools which are standalone CLI utilities, these are Python functions decorated with LangChain's `@tool` decorator for direct use by AI agents.

## Philosophy

### Agent Tools vs Management Tools

- **Agent Tools** (this directory): Functions that agents call during execution
  - LangChain `@tool` decorated functions
  - Used within LangGraph workflows
  - Return values directly to the agent
  - Part of the agent's action space

- **Management Tools** (`tools/phoenix/`): Standalone CLI utilities
  - Argparse-based command-line tools
  - Used for system management and operations
  - Return JSON for composition
  - External to agent workflows

## Available Tools

### greeting_tools.py

Multi-language greeting functions for the Hello Phoenix demo agent.

```python
@tool
def hello_english(name: str) -> str:
    """Greet someone in English."""
    return f"Hello {name}"

@tool
def hello_spanish(name: str) -> str:
    """Greet someone in Spanish."""
    return f"Hola {name}"

@tool
def hello_mandarin(name: str) -> str:
    """Greet someone in Mandarin Chinese."""
    return f"你好 {name}"

@tool
def hello_hebrew(name: str) -> str:
    """Greet someone in Hebrew."""
    return f"שלום {name}"
```

## Usage in LangGraph

These tools are integrated into LangGraph agents via the `ToolNode`:

```python
from tools.agent.greeting_tools import get_all_tools
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph

# Get all available tools
tools = get_all_tools()

# Bind tools to LLM
llm_with_tools = llm.bind_tools(tools)

# Create tool node for execution
tool_node = ToolNode(tools)

# Add to workflow
workflow = StateGraph(AgentState)
workflow.add_node("tools", tool_node)
```

## Tool Structure

Each agent tool follows this pattern:

```python
from langchain_core.tools import tool

@tool
def tool_name(param1: type, param2: type) -> return_type:
    """Docstring describing what the tool does.
    
    This description is used by the LLM to understand
    when and how to use this tool.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
        
    Returns:
        Description of return value
    """
    # Tool implementation
    return result
```

## Key Differences from Management Tools

| Aspect | Agent Tools | Management Tools |
|--------|------------|-----------------|
| **Invocation** | Called by LLM during execution | Run via command line or scripts |
| **Interface** | Python function with type hints | Argparse CLI with flags |
| **Discovery** | LLM reads docstrings | `--context` flag returns JSON |
| **Output** | Direct Python objects | JSON strings |
| **Error Handling** | Python exceptions | JSON error responses |
| **Composition** | LangGraph workflow | Shell scripts or agent orchestration |

## Creating New Agent Tools

To add a new tool for agent use:

1. **Define the tool function**:
```python
@tool
def my_new_tool(input_data: str) -> dict:
    """Clear description of what this tool does.
    
    Args:
        input_data: What this parameter represents
        
    Returns:
        What the tool returns
    """
    # Implementation
    return {"result": processed_data}
```

2. **Add to tool registry**:
```python
def get_all_tools():
    """Get all tools as a list."""
    return [
        existing_tool_1,
        existing_tool_2,
        my_new_tool,  # Add your tool here
    ]
```

3. **Document the tool**:
   - Clear, concise docstring
   - Type hints for all parameters
   - Examples in the docstring if complex

## Integration with Phoenix Tracing

When these tools are executed within a LangGraph agent, they are automatically traced by Phoenix:

1. Tool invocations appear as spans in the trace
2. Input parameters are captured
3. Output values are recorded
4. Execution time is measured
5. Errors are tracked

This provides full observability of agent tool usage through the Phoenix dashboard.

## Best Practices

1. **Clear Naming**: Use descriptive function names that indicate the action
2. **Type Hints**: Always include type hints for parameters and return values
3. **Docstrings**: Write clear docstrings that help the LLM understand usage
4. **Error Handling**: Raise informative exceptions rather than returning error strings
5. **Idempotency**: Tools should be idempotent where possible
6. **Side Effects**: Document any side effects in the docstring

## Example: Adding a Math Tool

```python
from langchain_core.tools import tool
import math

@tool
def calculate_fibonacci(n: int) -> list[int]:
    """Calculate the Fibonacci sequence up to n terms.
    
    Args:
        n: Number of terms to calculate (must be positive)
        
    Returns:
        List of Fibonacci numbers
        
    Example:
        calculate_fibonacci(5) returns [0, 1, 1, 2, 3]
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")
    
    if n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[-1] + sequence[-2])
    
    return sequence

# Add to get_all_tools() function
def get_all_tools():
    return [
        hello_english,
        hello_spanish,
        hello_mandarin,
        hello_hebrew,
        calculate_fibonacci,  # New tool added
    ]
```

## Testing Agent Tools

Test tools independently before integration:

```python
# Direct testing
from tools.agent.greeting_tools import hello_english

result = hello_english("Alice")
assert result == "Hello Alice"

# Test with LangChain
from langchain_core.tools import ToolException

try:
    result = my_tool.invoke({"param": "value"})
except ToolException as e:
    print(f"Tool error: {e}")
```

## Observability

When running with Phoenix tracing enabled, you can observe:

- Tool selection by the LLM
- Parameters passed to tools
- Execution duration
- Return values
- Error traces
- Tool usage patterns over time

View these in the Phoenix dashboard at `http://localhost:6006` under your project's traces.

## Future Enhancements

- [ ] Add tool versioning for backward compatibility
- [ ] Implement tool result caching for expensive operations
- [ ] Create tool categories for better organization
- [ ] Add tool usage analytics
- [ ] Implement tool permission levels
- [ ] Create tool testing framework
- [ ] Add async tool support for long-running operations