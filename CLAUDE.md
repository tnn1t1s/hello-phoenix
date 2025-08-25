# Hello Phoenix - Arize Phoenix Integration

## Project Overview
Hello World application for Arize Phoenix observability platform running on localhost:6006

## Tech Stack
- Arize Phoenix: LLM observability & monitoring
- Python: Primary language
- OpenAI/LLM integration
- Phoenix Client: REST API interactions

## Local Development

### Prerequisites
- Python 3.8+
- Arize Phoenix running on localhost:6006
- API credentials in .env

### Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Configure .env with necessary credentials
3. Start Phoenix: `phoenix serve` (port 6006)
4. Run application: `python main.py`

## Environment Variables
- `PHOENIX_HOST`: Phoenix server URL (default: http://localhost:6006)
- `OPENAI_API_KEY`: OpenAI API key (if using OpenAI)
- Additional LLM credentials as needed

## Key Features
- Phoenix tracing integration
- LLM call monitoring
- Performance metrics collection
- Span tracking
- REST API client for programmatic access

## Phoenix Client Usage

The `arize-phoenix-client` package provides programmatic access to Phoenix server via REST API:

### Installation
```bash
pip install arize-phoenix-client
```

### Key Capabilities
- **Trace Management**: Query, filter, and analyze traces
- **Span Operations**: Access individual spans within traces
- **Evaluations**: Add and retrieve trace/span evaluations
- **Annotations**: Programmatically annotate traces for analysis
- **Prompts**: Manage prompt templates and versions
- **Projects**: Organize traces into projects

### Common Operations

```python
from phoenix.client import Client

# Connect to Phoenix server
client = Client(endpoint="http://localhost:6006")

# Get traces for a project
traces = client.get_traces(project_name="hello-phoenix")

# Add evaluations to traces
client.add_evaluations(
    project_name="hello-phoenix",
    evaluations=[
        {"trace_id": "...", "metric": "quality", "value": 4.5}
    ]
)

# Query spans with filters
spans = client.get_spans(
    project_name="hello-phoenix",
    filter_condition="span_kind == 'LLM'"
)
```

### REST API Endpoints
- `POST /v1/evaluations`: Add trace or span evaluations
- `GET /v1/evaluations`: Fetch evaluations from a project
- `GET /v1/traces`: Query traces with filters
- `GET /v1/spans`: Query spans with filters
- `POST /v1/annotations`: Add annotations to traces
- `GET /v1/projects`: List available projects

## Commands

### Phoenix Server
- `phoenix serve`: Start Phoenix server on localhost:6006

### Demo Scripts
- `python main.py`: Run original hello world example (hello-phoenix project)
- `python bin/multi_call_greeter.py`: 4 separate LLM calls demo (multi-call-greeter project)
- `python bin/single_call_greeter.py`: 1 LLM call with 4 tools demo (single-call-greeter project)

### Phoenix Management (via justfile)
- `just list-all-projects`: List all Phoenix projects
- `just list-project-traces <project>`: List traces for a project
- `just delete-project-traces <project>`: Delete all traces from a project
- `just show-all-contexts`: Show tool capabilities for agents

### Testing
- `pytest`: Run all tests
- `just verify-tools`: Verify all tools have --context flag

## Notes
- Phoenix dashboard: http://localhost:6006
- Traces viewable in real-time
- Supports multiple LLM providers
- Client enables automated evaluation workflows

## Agent-Oriented Development Philosophy (2025)

### Core Principles

In 2025, we build for AI agents as first-class consumers. This means:

1. **Composable Tools Over Monolithic Scripts**
   - Each tool does ONE thing well
   - Tools are discovered and composed by agents at runtime
   - No hardcoded workflows or orchestration logic
   - Tools communicate via structured JSON

2. **Clear Grammar Patterns**
   - All tools use argparse with consistent patterns
   - Verb-Adjective-Noun command semantics (e.g., `delete-all-traces`, `list-recent-spans`)
   - Predictable parameter names across tools
   - Structured output formats (JSON by default)

3. **Agent Discovery Protocol**
   - Every tool supports `--context` flag for capability discovery
   - Returns JSON describing inputs, outputs, and purpose
   - Distinct from `--help` which is human-readable
   - Enables agents to understand tool capabilities without execution

4. **No Hardcoded Names or Heuristics**
   - No assumptions about project names, trace IDs, or metrics
   - All values passed as parameters
   - Configuration via environment or explicit args
   - Tools are stateless and idempotent where possible

### Tool Development Standards

```python
# Every tool MUST implement:
if args.context:
    print(json.dumps({
        "capability": "tool_action",
        "inputs": {...},
        "outputs": {...},
        "description": "What this tool does"
    }))
    return
```

### Justfile Semantics

Commands follow verb-adjective-noun pattern:
- `just list-all-projects`
- `just delete-project-traces hello-phoenix`
- `just add-trace-evaluation project-name trace-id metric value`

### Tool Directory Structure

```
tools/
├── agent/                # Tools used by LangGraph agents
│   └── greeting_tools.py # Multi-language greeting functions
└── phoenix/              # Phoenix management CLI tools
    ├── delete_traces.py  # Delete traces from project
    ├── list_traces.py    # Query and filter traces
    └── list_projects.py  # List available projects
```

- **agent/**: Tools that agents use for their workflows (LangChain @tool decorated functions)
- **phoenix/**: Composable CLI tools for Phoenix server management (argparse-based with --context)

Each Phoenix tool is independently executable and agent-composable.

## Project Structure

```
hello-phoenix/
├── bin/                      # Demo scripts showing different patterns
│   ├── multi_call_greeter.py  # 4 LLM calls (one per language)
│   └── single_call_greeter.py # 1 LLM call (uses 4 tools)
├── src/hello_phoenix/        # Core application code
│   ├── agent.py             # LangGraph agent implementation
│   └── tracing.py           # Phoenix tracing setup
├── tools/                    # Composable tools directory
│   ├── agent/               # LangChain tools for agents
│   │   └── greeting_tools.py # Multi-language greeting functions
│   └── phoenix/             # Phoenix management CLI tools
│       ├── list_projects.py # List all projects
│       ├── list_traces.py   # List traces in a project
│       └── delete_traces.py # Clear traces from project
├── justfile                  # Task runner with semantic commands
├── main.py                   # Original demo script
└── requirements.txt          # Python dependencies
```

## Key Implementation Details

### GraphQL-First Approach
All Phoenix management tools use direct GraphQL queries instead of the Python client library. This provides:
- Zero dependency on `arize-phoenix-client`
- Direct control over queries
- Better understanding of Phoenix internals
- Lighter weight implementation

### Multiple Phoenix Projects
The application creates separate Phoenix projects for different demos:
- `hello-phoenix`: Original demo
- `multi-call-greeter`: Shows 4 separate LLM calls
- `single-call-greeter`: Shows 1 LLM call with multiple tools

This allows easy comparison of different agent patterns in the Phoenix UI.