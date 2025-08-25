#!/usr/bin/env just --justfile

# Phoenix Management Commands - Agent-Composable Tools
# Following verb-adjective-noun semantics for predictable grammar

# List Operations
list-all-projects:
    @python tools/phoenix/list_projects.py

list-project-traces project:
    @python tools/phoenix/list_traces.py --project {{project}}

list-recent-traces project limit="10":
    @python tools/phoenix/list_traces.py --project {{project}} --limit {{limit}}

# Delete Operations  
delete-project-traces project:
    @python tools/phoenix/delete_traces.py --project {{project}}

delete-all-traces project:
    @python tools/phoenix/delete_traces.py --project {{project}} --confirm

# Discovery Operations (for agents)
show-phoenix-context tool:
    @python tools/phoenix/{{tool}}.py --context

show-agent-context tool:
    @python tools/agent/{{tool}}.py --context

show-all-contexts:
    @echo "=== Phoenix Tool Contexts ==="
    @for tool in tools/phoenix/*.py; do \
        echo "\n--- $$(basename $$tool .py) ---" && \
        python $$tool --context; \
    done
    @echo "\n=== Agent Tool Contexts ==="
    @for tool in tools/agent/*.py; do \
        echo "\n--- $$(basename $$tool .py) ---" && \
        python $$tool --context 2>/dev/null || echo "No context flag"; \
    done

# Project Operations
check-project-exists project:
    @python tools/phoenix/list_projects.py | jq -r '.projects[] | select(.name=="{{project}}") | .name' || echo "Project not found"

count-project-traces project:
    @python tools/phoenix/list_traces.py --project {{project}} | jq -r '.count'

# Development Operations
verify-tools:
    @echo "Verifying Phoenix tools have --context flag..."
    @for tool in tools/phoenix/*.py; do \
        echo -n "$$(basename $$tool): " && \
        python $$tool --context > /dev/null 2>&1 && echo "✓" || echo "✗"; \
    done
    @echo "\nVerifying Agent tools..."
    @for tool in tools/agent/*.py; do \
        echo -n "$$(basename $$tool): " && \
        python $$tool --context > /dev/null 2>&1 && echo "✓" || echo "✗"; \
    done

# Server Operations
start-phoenix:
    phoenix serve

check-phoenix:
    @curl -s http://localhost:6006 > /dev/null && echo "Phoenix is running" || echo "Phoenix is not running"


# Help
help:
    @echo "Phoenix Management Tools - Agent-Composable Commands"
    @echo ""
    @echo "List Operations:"
    @echo "  just list-all-projects              - List all Phoenix projects"
    @echo "  just list-project-traces <project>  - List traces for a project"
    @echo ""
    @echo "Delete Operations:"
    @echo "  just delete-project-traces <project> - Delete all traces from project"
    @echo ""
    @echo "Discovery:"
    @echo "  just show-tool-context <tool>       - Show tool capabilities (for agents)"
    @echo "  just show-all-contexts               - Show all tool capabilities"
    @echo ""
    @echo "Development:"
    @echo "  just verify-tools                    - Verify all tools are properly configured"