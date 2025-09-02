"""Shared GraphQL utilities for Phoenix tools."""

# pylint: disable=import-error
import requests
# pylint: enable=import-error


def get_graphql_endpoint(endpoint):
    """Get the GraphQL endpoint URL from base endpoint."""
    return f"{endpoint}/graphql"


def execute_graphql_query(endpoint, query, variables=None):
    """Execute a GraphQL query against Phoenix server.
    
    Args:
        endpoint: Phoenix server base endpoint
        query: GraphQL query string
        variables: Optional query variables
        
    Returns:
        Response object from requests.post
    """
    graphql_endpoint = get_graphql_endpoint(endpoint)
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    
    return requests.post(
        graphql_endpoint,
        json=payload,
        headers={"Content-Type": "application/json"},
    )


def get_project_id(project_name, endpoint):
    """Get project ID by name using GraphQL.
    
    Args:
        project_name: Name of the Phoenix project
        endpoint: Phoenix server endpoint
        
    Returns:
        Project ID string or None if not found
    """
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
    
    response = execute_graphql_query(endpoint, query)
    
    if response.status_code == 200:
        result = response.json()
        if "data" in result:
            edges = result["data"]["projects"]["edges"]
            for edge in edges:
                if edge["node"]["name"] == project_name:
                    return edge["node"]["id"]
    return None


def get_project_input_schema():
    """Get common project input schema for tool capabilities."""
    return {
        "project": {
            "type": "string",
            "required": True,
            "description": "Name of the Phoenix project",
        }
    }


def get_endpoint_input_schema():
    """Get common endpoint input schema for tool capabilities."""
    return {
        "endpoint": {
            "type": "string",
            "required": False,
            "description": "Phoenix server endpoint (default: from PHOENIX_HOST env)",
        }
    }