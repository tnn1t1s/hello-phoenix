#!/usr/bin/env python3
"""List all Phoenix projects."""

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
        "capability": "list_projects",
        "inputs": {
            "endpoint": {
                "type": "string",
                "required": False,
                "description": "Phoenix server endpoint (default: from PHOENIX_HOST env)"
            }
        },
        "outputs": {
            "success": "boolean",
            "message": "string",
            "projects": "array",
            "count": "integer"
        },
        "description": "Lists all available Phoenix projects"
    }


def list_projects(endpoint=None):
    """List all Phoenix projects using GraphQL API."""
    
    if not endpoint:
        endpoint = os.getenv("PHOENIX_HOST", "http://localhost:6006")
    
    try:
        # GraphQL query to get all projects
        graphql_endpoint = f"{endpoint}/graphql"
        query = """
        query GetProjects {
            projects {
                edges {
                    node {
                        id
                        name
                        createdAt
                        traceCount
                        recordCount
                        tokenCountTotal
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
        
        if response.status_code != 200:
            return {
                "success": False,
                "message": f"HTTP error {response.status_code}: {response.text}",
                "projects": [],
                "count": 0
            }
        
        result = response.json()
        
        if "errors" in result and result["errors"]:
            return {
                "success": False,
                "message": f"GraphQL error: {result['errors'][0]['message']}",
                "projects": [],
                "count": 0
            }
        
        # Extract projects from GraphQL response
        edges = result.get("data", {}).get("projects", {}).get("edges", [])
        
        if not edges:
            return {
                "success": True,
                "message": "No projects found",
                "projects": [],
                "count": 0
            }
        
        # Convert projects to serializable format
        project_list = []
        for edge in edges:
            node = edge.get("node", {})
            project_dict = {
                "name": node.get("name"),
                "id": node.get("id"),
                "created_at": node.get("createdAt"),
                "trace_count": node.get("traceCount"),
                "record_count": node.get("recordCount"),
                "token_count_total": node.get("tokenCountTotal")
            }
            project_list.append(project_dict)
        
        return {
            "success": True,
            "message": f"Found {len(project_list)} projects",
            "projects": project_list,
            "count": len(project_list)
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "projects": [],
            "count": 0
        }


def main():
    parser = argparse.ArgumentParser(description="List all Phoenix projects")
    parser.add_argument("--endpoint", help="Phoenix server endpoint (default: from PHOENIX_HOST env)")
    parser.add_argument("--context", action="store_true", help="Return tool capabilities as JSON")
    
    args = parser.parse_args()
    
    if args.context:
        print(json.dumps(get_context(), indent=2))
        return 0
    
    # List projects
    result = list_projects(args.endpoint)
    
    # Output as JSON for agent consumption
    print(json.dumps(result, indent=2))
    
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())