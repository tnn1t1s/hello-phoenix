#!/usr/bin/env python3
"""List traces from a Phoenix project with optional filters."""

import argparse
import json
import os
import sys
from pathlib import Path
import requests

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

load_dotenv()


def get_context():
    """Return tool capabilities for agent discovery."""
    return {
        "capability": "list_traces",
        "inputs": {
            "project": {
                "type": "string",
                "required": True,
                "description": "Name of the Phoenix project"
            },
            "limit": {
                "type": "integer",
                "required": False,
                "description": "Maximum number of traces to return"
            },
            "filter": {
                "type": "string",
                "required": False,
                "description": "Filter condition for traces"
            },
            "endpoint": {
                "type": "string",
                "required": False,
                "description": "Phoenix server endpoint (default: from PHOENIX_HOST env)"
            }
        },
        "outputs": {
            "success": "boolean",
            "message": "string",
            "traces": "array",
            "count": "integer",
            "project": "string"
        },
        "description": "Lists traces from the specified Phoenix project with optional filtering"
    }


def get_project_id(project_name, endpoint):
    """Get project ID by name using GraphQL."""
    graphql_endpoint = f"{endpoint}/graphql"
    query = """
    query GetProjects {
        projects {
            edges {
                node {
                    id
                    name
                }
            }
        }
    }
    """
    
    response = requests.post(
        graphql_endpoint,
        json={"query": query},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        if "data" in result:
            edges = result["data"]["projects"]["edges"]
            for edge in edges:
                if edge["node"]["name"] == project_name:
                    return edge["node"]["id"]
    return None


def list_traces(project_name, limit=None, filter_condition=None, endpoint=None):
    """List traces from a Phoenix project using GraphQL API."""
    
    if not endpoint:
        endpoint = os.getenv("PHOENIX_HOST", "http://localhost:6006")
    
    try:
        # First get the project ID
        project_id = get_project_id(project_name, endpoint)
        
        if not project_id:
            return {
                "success": False,
                "message": f"Project '{project_name}' not found",
                "traces": [],
                "count": 0,
                "project": project_name
            }
        
        # GraphQL query to get traces/spans for the project
        graphql_endpoint = f"{endpoint}/graphql"
        
        # Build query with optional limit
        limit_arg = f"first: {limit}" if limit else ""
        
        query = f"""
        query GetTraces {{
            project(id: "{project_id}") {{
                spans({limit_arg}) {{
                    edges {{
                        node {{
                            id
                            context {{
                                traceId
                            }}
                            name
                            statusCode
                            startTime
                            endTime
                            latencyMs
                            tokenCountTotal
                            tokenCountPrompt
                            tokenCountCompletion
                        }}
                    }}
                }}
            }}
        }}
        """
        
        response = requests.post(
            graphql_endpoint,
            json={"query": query},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code != 200:
            return {
                "success": False,
                "message": f"HTTP error {response.status_code}: {response.text}",
                "traces": [],
                "count": 0,
                "project": project_name
            }
        
        result = response.json()
        
        if "errors" in result and result["errors"]:
            return {
                "success": False,
                "message": f"GraphQL error: {result['errors'][0]['message']}",
                "traces": [],
                "count": 0,
                "project": project_name
            }
        
        # Extract spans and group by trace ID
        spans_edges = result.get("data", {}).get("project", {}).get("spans", {}).get("edges", [])
        
        if not spans_edges:
            return {
                "success": True,
                "message": f"No traces found in project '{project_name}'",
                "traces": [],
                "count": 0,
                "project": project_name
            }
        
        # Group spans by trace ID to get unique traces
        traces_dict = {}
        for edge in spans_edges:
            node = edge.get("node", {})
            trace_id = node.get("context", {}).get("traceId")
            if trace_id and trace_id not in traces_dict:
                traces_dict[trace_id] = {
                    "trace_id": trace_id,
                    "first_span_name": node.get("name"),
                    "start_time": node.get("startTime"),
                    "latency_ms": node.get("latencyMs"),
                    "token_count_total": node.get("tokenCountTotal"),
                    "status_code": node.get("statusCode")
                }
        
        trace_list = list(traces_dict.values())
        
        return {
            "success": True,
            "message": f"Found {len(trace_list)} traces in project '{project_name}'",
            "traces": trace_list,
            "count": len(trace_list),
            "project": project_name
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "traces": [],
            "count": 0,
            "project": project_name
        }


def main():
    parser = argparse.ArgumentParser(description="List traces from a Phoenix project")
    parser.add_argument("--project", required=True, help="Project name")
    parser.add_argument("--limit", type=int, help="Maximum number of traces to return")
    parser.add_argument("--filter", dest="filter_condition", help="Filter condition for traces")
    parser.add_argument("--endpoint", help="Phoenix server endpoint (default: from PHOENIX_HOST env)")
    parser.add_argument("--context", action="store_true", help="Return tool capabilities as JSON")
    
    args = parser.parse_args()
    
    if args.context:
        print(json.dumps(get_context(), indent=2))
        return 0
    
    # List traces
    result = list_traces(
        args.project, 
        args.limit, 
        args.filter_condition,
        args.endpoint
    )
    
    # Output as JSON for agent consumption
    print(json.dumps(result, indent=2))
    
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())