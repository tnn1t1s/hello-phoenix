# Phoenix Management Tools

## Overview

This directory contains composable, agent-friendly tools for managing Arize Phoenix observability platform via its GraphQL API. These tools follow modern (2025) agent-oriented development practices where AI agents discover and compose tools dynamically.

## Philosophy

### Core Principles

1. **Single Responsibility**: Each tool does ONE thing well
2. **Agent Discovery**: Every tool supports `--context` flag for capability discovery
3. **GraphQL Native**: Direct GraphQL API calls, no Python client dependencies
4. **JSON First**: All output is structured JSON for agent consumption
5. **No Orchestration**: Tools are atomic - agents compose workflows

### Why GraphQL Over Python Client?

- **Zero Dependencies**: No need for `arize-phoenix-client` package
- **Direct Control**: Explicit queries for exactly what we need
- **Lighter Weight**: Just `requests` library instead of full SDK
- **Version Agnostic**: Works with any Phoenix server version that supports GraphQL
- **Transparent**: Clear understanding of what each tool does

## Available Tools

### list_projects.py
Lists all Phoenix projects with metadata.

```bash
# List all projects
python tools/phoenix/list_projects.py

# Get tool capabilities (for agents)
python tools/phoenix/list_projects.py --context

# Output includes: name, id, created_at, trace_count, token_count_total
```

### list_traces.py
Lists traces from a specific project.

```bash
# List all traces in a project
python tools/phoenix/list_traces.py --project hello-phoenix

# Limit number of traces
python tools/phoenix/list_traces.py --project hello-phoenix --limit 10

# Get tool capabilities
python tools/phoenix/list_traces.py --context
```

**Note**: Currently uses spans query as Phoenix doesn't expose traces directly via GraphQL.

### delete_traces.py
Deletes all traces from a project while keeping the project intact.

```bash
# Delete all traces from a project
python tools/phoenix/delete_traces.py --project hello-phoenix

# Skip confirmation (for automation)
python tools/phoenix/delete_traces.py --project hello-phoenix --confirm

# Get tool capabilities
python tools/phoenix/delete_traces.py --context
```

## Implementation Details

### GraphQL Endpoint
All tools connect to Phoenix GraphQL API at `{PHOENIX_HOST}/graphql` (default: `http://localhost:6006/graphql`)

### Key GraphQL Queries/Mutations

```graphql
# List projects
query GetProjects {
  projects {
    edges {
      node {
        id
        name
        traceCount
        recordCount
        tokenCountTotal
      }
    }
  }
}

# Clear project (delete all traces)
mutation ClearProject($input: ClearProjectInput!) {
  clearProject(input: $input) {
    __typename
  }
}
```

### Environment Variables

- `PHOENIX_HOST`: Phoenix server URL (default: `http://localhost:6006`)

### Tool Discovery Protocol

Every tool implements the `--context` flag that returns:

```json
{
  "capability": "tool_action",
  "inputs": {
    "param_name": {
      "type": "string|integer|boolean",
      "required": true|false,
      "description": "What this parameter does"
    }
  },
  "outputs": {
    "field_name": "type_description"
  },
  "description": "What this tool does"
}
```

This allows agents to:
1. Discover available tools
2. Understand their capabilities
3. Know required/optional parameters
4. Compose them into workflows

## Usage with Justfile

The project includes semantic commands in the justfile:

```bash
# List operations
just list-all-projects
just list-project-traces hello-phoenix

# Delete operations
just delete-project-traces hello-phoenix

# Discovery
just show-phoenix-context delete_traces
just show-all-contexts
```

## Error Handling

All tools return consistent JSON responses:

### Success Response
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {...},
  "count": 42
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error description",
  "data": [],
  "count": 0
}
```

## Agent Composition Example

An AI agent can discover and compose these tools:

```python
# Agent discovers available tools
tools = ["list_projects", "delete_traces", "list_traces"]

# Agent checks capabilities
for tool in tools:
    context = run_tool(f"{tool}.py", "--context")
    analyze_capabilities(context)

# Agent composes workflow
workflow = [
    ("list_projects.py", {}),  # See what projects exist
    ("list_traces.py", {"project": "hello-phoenix", "limit": 5}),  # Check traces
    ("delete_traces.py", {"project": "hello-phoenix"})  # Clean up
]

# Execute workflow
for tool, params in workflow:
    result = run_tool(tool, params)
    if not result["success"]:
        handle_error(result["message"])
```

## Extending the Tools

To add a new Phoenix management tool:

1. Create a new Python file in `tools/phoenix/`
2. Implement argparse with required parameters
3. Add `--context` flag that returns capability JSON
4. Use GraphQL queries/mutations via requests
5. Return structured JSON output
6. Update the justfile with semantic commands

### Template

```python
#!/usr/bin/env python3
"""Tool description."""

import argparse
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_context():
    """Return tool capabilities for agent discovery."""
    return {
        "capability": "action_name",
        "inputs": {...},
        "outputs": {...},
        "description": "What this tool does"
    }

def main():
    parser = argparse.ArgumentParser(description="Tool description")
    parser.add_argument("--context", action="store_true", 
                       help="Return tool capabilities as JSON")
    # Add other arguments
    
    args = parser.parse_args()
    
    if args.context:
        print(json.dumps(get_context(), indent=2))
        return 0
    
    # Tool implementation
    result = perform_action(args)
    print(json.dumps(result, indent=2))
    return 0 if result["success"] else 1

if __name__ == "__main__":
    sys.exit(main())
```

## Limitations

- Phoenix's GraphQL API doesn't expose all functionality (e.g., individual trace deletion)
- Some queries like `project(id:)` may not work in all Phoenix versions
- Traces are accessed indirectly through spans
- No pagination support yet for large datasets

## Future Improvements

- [ ] Add pagination support for large trace lists
- [ ] Implement selective trace deletion (by ID or time range)
- [ ] Add span-level querying tools
- [ ] Support for evaluation metrics
- [ ] Batch operations for efficiency
- [ ] WebSocket subscriptions for real-time updates