from mcp.server.fastmcp import FastMCP, Context
from typing import Dict, List, Optional, Union, Any
import os
import requests
import base64
import json
from datetime import datetime, timedelta

# Create an MCP server
mcp = FastMCP("Toggl API", dependencies=["requests", "python-dotenv"])

# Configuration
class TogglConfig:
    def __init__(self):
        self.api_token = os.environ.get("TOGGL_API_TOKEN", "")
        self.base_url_v8 = "https://api.track.toggl.com/api/v8"
        self.base_url_v9 = "https://api.track.toggl.com/api/v9"
        self.reports_api_v2 = "https://api.track.toggl.com/reports/api/v2"
        self.reports_api_v3 = "https://api.track.toggl.com/reports/api/v3"
        self.webhooks_api = "https://track.toggl.com/webhooks/api/v1"

config = TogglConfig()

# Auth and request helpers
def get_auth_header():
    """Create basic auth header with API token"""
    if not config.api_token:
        raise ValueError("API token not configured")
    
    auth_string = f"{config.api_token}:api_token"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()
    return {"Authorization": f"Basic {encoded_auth}"}

def make_request(method: str, url: str, data: dict = None, params: dict = None):
    """Make a request to Toggl API with proper authentication"""
    headers = get_auth_header()
    headers["Content-Type"] = "application/json"
    
    response = requests.request(
        method=method,
        url=url,
        headers=headers,
        json=data if data else None,
        params=params if params else None
    )
    
    # Check if request was successful
    response.raise_for_status()
    
    # Return parsed JSON if available
    if response.text:
        return response.json()
    return {"status": "success"}

# Resources
@mcp.resource("me://")
def get_current_user() -> str:
    """Get current user data"""
    url = f"{config.base_url_v8}/me"
    result = make_request("GET", url)
    return json.dumps(result, indent=2)

@mcp.resource("workspaces://")
def get_workspaces() -> str:
    """Get all workspaces for the current user"""
    url = f"{config.base_url_v8}/workspaces"
    result = make_request("GET", url)
    return json.dumps(result, indent=2)

@mcp.resource("workspaces://{workspace_id}")
def get_workspace(workspace_id: int) -> str:
    """Get details for a specific workspace"""
    url = f"{config.base_url_v8}/workspaces/{workspace_id}"
    result = make_request("GET", url)
    return json.dumps(result, indent=2)

@mcp.resource("workspaces://{workspace_id}/users")
def get_workspace_users(workspace_id: int) -> str:
    """Get all users in a workspace (requires admin access)"""
    url = f"{config.base_url_v8}/workspaces/{workspace_id}/users"
    result = make_request("GET", url)
    return json.dumps(result, indent=2)

@mcp.resource("workspaces://{workspace_id}/clients")
def get_workspace_clients(workspace_id: int) -> str:
    """Get all clients in a workspace"""
    url = f"{config.base_url_v8}/workspaces/{workspace_id}/clients"
    result = make_request("GET", url)
    return json.dumps(result, indent=2)

@mcp.resource("workspaces://{workspace_id}/projects")
def get_workspace_projects(workspace_id: int) -> str:
    """Get all projects in a workspace"""
    url = f"{config.base_url_v8}/workspaces/{workspace_id}/projects"
    params = {"active": "true"}
    result = make_request("GET", url, params=params)
    return json.dumps(result, indent=2)

@mcp.resource("workspaces://{workspace_id}/tasks")
def get_workspace_tasks(workspace_id: int) -> str:
    """Get all tasks in a workspace (premium feature)"""
    url = f"{config.base_url_v8}/workspaces/{workspace_id}/tasks"
    params = {"active": "true"}
    result = make_request("GET", url, params=params)
    return json.dumps(result, indent=2)

@mcp.resource("workspaces://{workspace_id}/tags")
def get_workspace_tags(workspace_id: int) -> str:
    """Get all tags in a workspace"""
    url = f"{config.base_url_v8}/workspaces/{workspace_id}/tags"
    result = make_request("GET", url)
    return json.dumps(result, indent=2)

@mcp.resource("time_entries://{time_entry_id}")
def get_time_entry(time_entry_id: int) -> str:
    """Get a specific time entry"""
    url = f"{config.base_url_v8}/time_entries/{time_entry_id}"
    result = make_request("GET", url)
    return json.dumps(result, indent=2)

@mcp.resource("time-entries:/current")
def get_current_time_entry() -> str:
    """Get the currently running time entry if any"""
    url = f"{config.base_url_v8}/time_entries/current"
    result = make_request("GET", url)
    return json.dumps(result, indent=2)

@mcp.resource("projects://{project_id}")
def get_project(project_id: int) -> str:
    """Get details for a specific project"""
    url = f"{config.base_url_v8}/projects/{project_id}"
    result = make_request("GET", url)
    return json.dumps(result, indent=2)

@mcp.resource("clients://{client_id}")
def get_client(client_id: int) -> str:
    """Get details for a specific client"""
    url = f"{config.base_url_v8}/clients/{client_id}"
    result = make_request("GET", url)
    return json.dumps(result, indent=2)

@mcp.resource("tags://{tag_id}")
def get_tag(tag_id: int) -> str:
    """Get details for a specific tag"""
    url = f"{config.base_url_v8}/tags/{tag_id}"
    result = make_request("GET", url)
    return json.dumps(result, indent=2)

@mcp.resource("tasks://{task_id}")
def get_task(task_id: int) -> str:
    """Get details for a specific task"""
    url = f"{config.base_url_v8}/tasks/{task_id}"
    result = make_request("GET", url)
    return json.dumps(result, indent=2)

# Tools
@mcp.tool()
def get_weekly_report(
    workspace_id: int,
    since: Optional[str] = None,
    until: Optional[str] = None,
    user_agent: str = "TogglMCP",
) -> str:
    """Get weekly report data"""
    url = f"{config.reports_api_v2}/weekly"
    params = {
        "workspace_id": workspace_id,
        "user_agent": user_agent,
    }
    
    # Add optional parameters
    if since:
        params["since"] = since
    if until:
        params["until"] = until
    
    result = make_request("GET", url, params=params)
    return json.dumps(result, indent=2)

@mcp.tool()
def get_detailed_report(
    workspace_id: int,
    since: Optional[str] = None,
    until: Optional[str] = None,
    page: Optional[int] = 1,
    user_agent: str = "TogglMCP",
) -> str:
    """Get detailed report data"""
    url = f"{config.reports_api_v2}/details"
    params = {
        "workspace_id": workspace_id,
        "user_agent": user_agent,
        "page": page,
    }
    
    # Add optional parameters
    if since:
        params["since"] = since
    if until:
        params["until"] = until
    
    result = make_request("GET", url, params=params)
    return json.dumps(result, indent=2)

@mcp.tool()
def get_summary_report(
    workspace_id: int,
    since: Optional[str] = None,
    until: Optional[str] = None,
    grouping: Optional[str] = "projects",
    user_agent: str = "TogglMCP",
) -> str:
    """Get summary report data"""
    url = f"{config.reports_api_v2}/summary"
    params = {
        "workspace_id": workspace_id,
        "user_agent": user_agent,
        "grouping": grouping,
    }
    
    # Add optional parameters
    if since:
        params["since"] = since
    if until:
        params["until"] = until
    
    result = make_request("GET", url, params=params)
    return json.dumps(result, indent=2)

@mcp.tool()
def get_webhook_subscriptions(
    workspace_id: int,
    user_agent: str = "TogglMCP"
) -> str:
    """List available webhook subscriptions for a workspace"""
    url = f"{config.webhooks_api}/subscriptions/{workspace_id}"
    headers = get_auth_header()
    headers["User-Agent"] = user_agent
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return json.dumps(response.json(), indent=2)

# Prompts
@mcp.prompt()
def analyze_time_entries(workspace_id: int) -> str:
    """Create a prompt for analyzing time entries"""
    return f"""Please analyze the time entries for workspace {workspace_id}.
    
You can use the following resources:
- workspaces://{workspace_id}
- workspaces://{workspace_id}/projects
- workspaces://{workspace_id}/clients

And the following tools:
- get_weekly_report
- get_detailed_report
- get_summary_report

Please provide insights on time usage patterns and productivity.
"""

@mcp.prompt()
def project_analysis(project_id: int) -> str:
    """Create a prompt for analyzing a specific project"""
    return f"""Please analyze project {project_id}.
    
You can use the following resources:
- projects://{project_id}

And the following tools:
- get_summary_report

Please provide insights on project progress, time allocation, and any potential issues.
"""

if __name__ == "__main__":
    mcp.run() 