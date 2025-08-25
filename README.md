# Hello Phoenix - LangGraph + Arize Phoenix Integration Demo

A demonstration of modern (2025) agent-oriented development practices combining LangGraph agents with Arize Phoenix observability. This project showcases composable tools, GraphQL-based Phoenix management, and comparative tracing patterns.

## 🎯 Project Goals

1. **Demonstrate Phoenix Tracing**: Show how to instrument LangGraph agents with Phoenix for full observability
2. **Agent-Oriented Architecture**: Implement composable, discoverable tools following 2025 best practices
3. **Compare Agent Patterns**: Visualize the difference between multiple LLM calls vs single coordinated calls
4. **GraphQL-First Approach**: Manage Phoenix entirely through GraphQL API without Python client dependencies

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- Phoenix server (will be installed)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd hello-phoenix

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Running the Demos

```bash
# Start Phoenix server (in separate terminal)
phoenix serve

# Run the original demo (4 separate agent calls)
python main.py

# Run multi-call pattern (4 LLM calls, 4 tool calls)
python bin/multi_call_greeter.py

# Run single-call pattern (1 LLM call, 4 tool calls)
python bin/single_call_greeter.py

# View traces at http://localhost:6006
```

## 📊 Architecture Overview

### Core Components

```
┌─────────────────────┐
│   LangGraph Agent   │
│  (Multi-language)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Phoenix Tracing   │
│  (OpenTelemetry)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Phoenix Server    │
│  (localhost:6006)   │
└─────────────────────┘
```

### Project Structure

```
hello-phoenix/
├── bin/                        # Executable demo scripts
│   ├── multi_call_greeter.py   # Demonstrates 4 separate LLM calls
│   └── single_call_greeter.py  # Demonstrates 1 LLM call with 4 tools
│
├── src/hello_phoenix/          # Core application code
│   ├── agent.py                # LangGraph agent with greeting tools
│   └── tracing.py              # Phoenix tracing configuration
│
├── tools/                      # Composable tools (2025 pattern)
│   ├── agent/                  # LangChain tools for agents
│   │   ├── greeting_tools.py   # Multi-language greeting functions
│   │   └── README.md          # Agent tools documentation
│   │
│   └── phoenix/                # Phoenix management CLI tools
│       ├── list_projects.py    # List all Phoenix projects
│       ├── list_traces.py      # Query traces from projects
│       ├── delete_traces.py    # Clear traces (keep project)
│       └── README.md           # Phoenix tools documentation
│
├── justfile                    # Task automation (verb-adjective-noun)
├── main.py                     # Original demo script
├── CLAUDE.md                   # Project instructions for AI agents
└── requirements.txt            # Python dependencies
```

## 🛠️ Key Features

### 1. Multi-Language Greeting Agent

A LangGraph agent that can greet people in 4 languages using dedicated tools:
- English: `hello_english()`
- Spanish: `hello_spanish()`
- Mandarin: `hello_mandarin()`
- Hebrew: `hello_hebrew()`

### 2. Phoenix Observability

Full tracing of:
- LLM calls (OpenAI)
- Tool invocations
- Agent state transitions
- Token usage and costs
- Execution latency

### 3. Composable Phoenix Tools

GraphQL-based CLI tools following agent-oriented patterns:

```bash
# List all projects
python tools/phoenix/list_projects.py

# List traces in a project
python tools/phoenix/list_traces.py --project hello-phoenix

# Delete all traces (keeps project)
python tools/phoenix/delete_traces.py --project hello-phoenix

# Get tool capabilities (for AI agents)
python tools/phoenix/list_projects.py --context
```

### 4. Comparative Demos

Two patterns showcasing different agent architectures:

**Multi-Call Pattern** (`bin/multi_call_greeter.py`):
- 4 separate LLM calls
- Each call handles one language
- Higher token usage
- Simpler reasoning per call

**Single-Call Pattern** (`bin/single_call_greeter.py`):
- 1 coordinated LLM call
- Agent plans and executes all 4 greetings
- Lower token usage
- More complex reasoning

## 📈 Phoenix Projects

The demos create separate Phoenix projects for easy comparison:

| Project | Description | LLM Calls | Tool Calls | Token Usage |
|---------|-------------|-----------|------------|-------------|
| `hello-phoenix` | Original demo | 4 | 4 | ~1600 |
| `multi-call-greeter` | Separate calls pattern | 4 | 4 | ~2500 |
| `single-call-greeter` | Coordinated pattern | 1 | 4 | ~850 |

View all projects at http://localhost:6006

## 🔧 Development Philosophy

### Agent-Oriented Development (2025)

This project follows modern practices where AI agents are first-class consumers:

1. **Composable Tools**: Each tool does ONE thing well
2. **Discovery Protocol**: `--context` flag returns capabilities as JSON
3. **No Orchestration**: Tools are atomic; agents compose workflows
4. **GraphQL-First**: Direct API access without heavy client libraries

### Tool Development Standards

Every Phoenix management tool implements:
```python
# Agent discovery
if args.context:
    return {
        "capability": "tool_action",
        "inputs": {...},
        "outputs": {...},
        "description": "What this tool does"
    }
```

## 🧪 Testing

```bash
# Run tests
pytest

# Verify all tools support --context
just verify-tools

# Test Phoenix connection
just check-phoenix
```

## 📚 Documentation

- [`CLAUDE.md`](CLAUDE.md) - Detailed project instructions for AI agents
- [`tools/phoenix/README.md`](tools/phoenix/README.md) - Phoenix tools documentation
- [`tools/agent/README.md`](tools/agent/README.md) - Agent tools documentation

## 🎯 Learning Objectives

This project demonstrates:

1. **LangGraph Integration**: Building multi-tool agents with state management
2. **Phoenix Tracing**: Instrumenting LLM applications for observability
3. **GraphQL APIs**: Direct API interaction without client libraries
4. **Agent Patterns**: Comparing different approaches to multi-step tasks
5. **Modern Tooling**: Building AI-agent-friendly CLI tools
6. **Token Optimization**: Understanding trade-offs in agent architectures

## 🚦 Common Commands

```bash
# Start Phoenix server
phoenix serve

# Run demos
just list-all-projects           # See all Phoenix projects
just delete-project-traces hello-phoenix  # Clear traces
python bin/multi_call_greeter.py  # Run multi-call demo
python bin/single_call_greeter.py # Run single-call demo

# Development
just show-all-contexts           # Show tool capabilities
just verify-tools                # Verify tool standards
```

## 🤝 Contributing

This project serves as a reference implementation for:
- Phoenix + LangGraph integration
- Agent-oriented tool development
- GraphQL-based Phoenix management
- Comparative agent architectures

Feel free to extend with additional languages, tools, or Phoenix management capabilities.

## 📄 License

MIT

## 🙏 Acknowledgments

- [Arize Phoenix](https://github.com/Arize-ai/phoenix) - LLM observability platform
- [LangGraph](https://github.com/langchain-ai/langgraph) - Agent orchestration framework
- [OpenAI](https://openai.com) - LLM provider

---

Built with 🤖 by following 2025 agent-oriented development practices