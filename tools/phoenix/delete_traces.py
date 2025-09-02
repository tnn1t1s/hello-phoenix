#!/usr/bin/env python3
"""Delete all traces from a Phoenix project."""

import argparse
import json
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# pylint: disable=import-error,wrong-import-position
from dotenv import load_dotenv
from phoenix.graphql_utils import (
    get_project_id,
    execute_graphql_query,
    get_project_input_schema,
    get_endpoint_input_schema,
)
# pylint: enable=import-error,wrong-import-position

load_dotenv()


def get_context():
    """Return tool capabilities for agent discovery."""
    inputs = {}
    inputs.update(get_project_input_schema())
    inputs.update(get_endpoint_input_schema())
    inputs["confirm"] = {
        "type": "boolean",
        "required": False,
        "description": "Skip confirmation prompt",
    }
    
    return {
        "capability": "delete_all_traces",
        "inputs": inputs,
        "outputs": {
            "success": "boolean",
            "message": "string",
            "deleted_count": "integer",
            "project": "string",
        },
        "description": "Deletes all traces from the specified Phoenix project using GraphQL API (keeps project intact)",
    }


def get_trace_count(project_id, endpoint):
    """Get trace count for a project using GraphQL."""
    # Since project(id:) query doesn't work, get it from projects list
    query = """
    query GetProjects {
        projects {
            edges {
                node {
                    id
                    name
                    traceCount
                }
            }
        }
    }
    """

    response = execute_graphql_query(endpoint, query)

    if response.status_code == 200:
        result = response.json()
        if "data" in result and result["data"] and "projects" in result["data"]:
            edges = result["data"]["projects"]["edges"]
            for edge in edges:
                if edge["node"]["id"] == project_id:
                    return edge["node"].get("traceCount", 0) or 0
    return 0


def delete_traces(project_name, endpoint=None, confirm=False):
    """Delete all traces from a Phoenix project.

    Uses the Phoenix GraphQL API to clear all traces from a project
    while keeping the project intact.
    """

    if not endpoint:
        endpoint = os.getenv("PHOENIX_HOST", "http://localhost:6006")

    try:
        # Get project ID
        project_id = get_project_id(project_name, endpoint)

        if not project_id:
            return {
                "success": False,
                "message": f"Project '{project_name}' not found",
                "deleted_count": 0,
                "project": project_name,
            }

        # Get trace count before deletion
        trace_count = get_trace_count(project_id, endpoint)

        if trace_count == 0:
            return {
                "success": True,
                "message": f"No traces found in project '{project_name}'",
                "deleted_count": 0,
                "project": project_name,
            }

        # Use GraphQL mutation to clear the project
        mutation = """
        mutation ClearProject($input: ClearProjectInput!) {
            clearProject(input: $input) {
                __typename
            }
        }
        """

        variables = {"input": {"id": project_id}}

        response = execute_graphql_query(endpoint, mutation, variables)

        if response.status_code == 200:
            result = response.json()
            if (
                result
                and "data" in result
                and result["data"]
                and ("errors" not in result or not result["errors"])
            ):
                return {
                    "success": True,
                    "message": f"Successfully deleted {trace_count} traces from project '{project_name}'",
                    "deleted_count": trace_count,
                    "project": project_name,
                }
            else:
                error_msg = "Unknown error"
                if result and "errors" in result and result["errors"]:
                    error_msg = result["errors"][0].get("message", "Unknown error")
                return {
                    "success": False,
                    "message": f"GraphQL error: {error_msg}",
                    "deleted_count": 0,
                    "project": project_name,
                }
        else:
            return {
                "success": False,
                "message": f"HTTP error {response.status_code}: {response.text}",
                "deleted_count": 0,
                "project": project_name,
            }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "deleted_count": 0,
            "project": project_name,
        }


def main():
    """Main function for CLI execution."""
    parser = argparse.ArgumentParser(
        description="Delete all traces from a Phoenix project"
    )
    parser.add_argument("--project", required=True, help="Project name")
    parser.add_argument(
        "--endpoint", help="Phoenix server endpoint (default: from PHOENIX_HOST env)"
    )
    parser.add_argument(
        "--confirm", action="store_true", help="Skip confirmation prompt"
    )
    parser.add_argument(
        "--context", action="store_true", help="Return tool capabilities as JSON"
    )

    args = parser.parse_args()

    if args.context:
        print(json.dumps(get_context(), indent=2))
        return 0

    # Execute deletion
    result = delete_traces(args.project, args.endpoint, args.confirm)

    # Output as JSON for agent consumption
    print(json.dumps(result, indent=2))

    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())