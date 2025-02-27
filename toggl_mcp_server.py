import base64
import json
import os
from typing import List, Optional

import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Create an MCP server
mcp = FastMCP("Toggl API", dependencies=["requests", "python-dotenv"])


# Configuration
class TogglConfig:
    def __init__(self):
        self.api_key = os.environ.get("TOGGL_API_KEY")
        self.base_url_v9 = "https://api.track.toggl.com/api/v9"
        self.reports_api_v2 = "https://api.track.toggl.com/reports/api/v2"
        self.reports_api_v3 = "https://api.track.toggl.com/reports/api/v3"
        self.webhooks_api = "https://track.toggl.com/webhooks/api/v1"
        self.insights_api = "https://api.track.toggl.com/insights/api/v1"


config = TogglConfig()


# If you need debugging, use a file instead:
# def log_to_file(message):
#     with open("mcp_debug.log", "a") as f:
#         f.write(f"{message}\n")


# Auth and request helpers
def get_auth_header():
    """Create basic auth header with token, or email and password"""
    if config.api_key:
        # API token authentication (preferred)
        auth_string = f"{config.api_key}:api_token"
        # log_to_file("Using API token authentication")
    else:
        raise ValueError(
            "API key not configured. Set TOGGL_API_KEY environment variable."
        )

    encoded_auth = base64.b64encode(auth_string.encode()).decode()
    # log_to_file(f"Generated auth: {encoded_auth}")  # Log to file instead of stdout
    return {"Authorization": f"Basic {encoded_auth}"}


def make_request(method: str, url: str, data: dict = None, params: dict = None):
    """Make a request to Toggl API with proper authentication"""
    headers = get_auth_header()
    headers["Content-Type"] = "application/json"

    # Debug: Print request details
    # log_to_file(f"Request URL: {url}")
    # log_to_file(f"Request Headers: {headers}")

    response = requests.request(
        method=method,
        url=url,
        headers=headers,
        json=data if data else None,
        params=params if params else None,
    )

    # Debug: Print response details
    # log_to_file(f"Response Status: {response.status_code}")
    # log_to_file(f"Response Text: {response.text[:200]}...")  # Print first 200 chars

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
    url = f"{config.base_url_v9}/me"
    try:
        result = make_request("GET", url)
        return json.dumps(result, indent=2)
    except Exception as e:
        # log_to_file(f"Error getting user data: {e}")
        # Return error but don't crash the server
        return json.dumps({"error": str(e)})


@mcp.resource("workspaces://")
def get_workspaces() -> str:
    """Get all workspaces for the current user"""
    url = f"{config.base_url_v9}/workspaces"
    result = make_request("GET", url)
    return json.dumps(result, indent=2)


@mcp.resource("workspaces://{workspace_id}")
def get_workspace(workspace_id: int) -> str:
    """Get details for a specific workspace"""
    url = f"{config.base_url_v9}/workspaces/{workspace_id}"
    result = make_request("GET", url)
    return json.dumps(result, indent=2)


@mcp.resource("workspaces://{workspace_id}/users")
def get_workspace_users(workspace_id: int) -> str:
    """Get all users in a workspace (requires admin access)"""
    url = f"{config.base_url_v9}/workspaces/{workspace_id}/users"
    result = make_request("GET", url)
    return json.dumps(result, indent=2)


@mcp.resource("workspaces://{workspace_id}/clients")
def get_workspace_clients(workspace_id: int) -> str:
    """Get all clients in a workspace"""
    url = f"{config.base_url_v9}/workspaces/{workspace_id}/clients"
    result = make_request("GET", url)
    return json.dumps(result, indent=2)


@mcp.resource("workspaces://{workspace_id}/projects")
def get_workspace_projects(workspace_id: int) -> str:
    """Get all projects in a workspace"""
    url = f"{config.base_url_v9}/workspaces/{workspace_id}/projects"
    params = {"active": "true"}
    result = make_request("GET", url, params=params)
    return json.dumps(result, indent=2)


@mcp.resource("workspaces://{workspace_id}/tasks")
def get_workspace_tasks(workspace_id: int) -> str:
    """Get all tasks in a workspace (premium feature)"""
    url = f"{config.base_url_v9}/workspaces/{workspace_id}/tasks"
    params = {"active": "true"}
    result = make_request("GET", url, params=params)
    return json.dumps(result, indent=2)


@mcp.resource("workspaces://{workspace_id}/tags")
def get_workspace_tags(workspace_id: int) -> str:
    """Get all tags in a workspace"""
    url = f"{config.base_url_v9}/workspaces/{workspace_id}/tags"
    result = make_request("GET", url)
    return json.dumps(result, indent=2)


@mcp.resource("time_entries://{time_entry_id}")
def get_time_entry(time_entry_id: int) -> str:
    """Get a specific time entry"""
    url = f"{config.base_url_v9}/time_entries/{time_entry_id}"
    result = make_request("GET", url)
    return json.dumps(result, indent=2)


@mcp.resource("time-entries:/current")
def get_current_time_entry() -> str:
    """Get the currently running time entry if any"""
    url = f"{config.base_url_v9}/time_entries/current"
    result = make_request("GET", url)
    return json.dumps(result, indent=2)


@mcp.resource("projects://{project_id}")
def get_project(project_id: int) -> str:
    """Get details for a specific project"""
    url = f"{config.base_url_v9}/projects/{project_id}"
    result = make_request("GET", url)
    return json.dumps(result, indent=2)


@mcp.resource("clients://{client_id}")
def get_client(client_id: int) -> str:
    """Get details for a specific client"""
    url = f"{config.base_url_v9}/clients/{client_id}"
    result = make_request("GET", url)
    return json.dumps(result, indent=2)


@mcp.resource("tags://{tag_id}")
def get_tag(tag_id: int) -> str:
    """Get details for a specific tag"""
    url = f"{config.base_url_v9}/tags/{tag_id}"
    result = make_request("GET", url)
    return json.dumps(result, indent=2)


@mcp.resource("tasks://{task_id}")
def get_task(task_id: int) -> str:
    """Get details for a specific task"""
    url = f"{config.base_url_v9}/tasks/{task_id}"
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
def get_webhook_subscriptions(workspace_id: int, user_agent: str = "TogglMCP") -> str:
    """List available webhook subscriptions for a workspace"""
    url = f"{config.webhooks_api}/subscriptions/{workspace_id}"
    headers = get_auth_header()
    headers["User-Agent"] = user_agent

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return json.dumps(response.json(), indent=2)


# New Insights API tools
@mcp.tool()
def get_projects_data_trends(
    workspace_id: int,
    start_date: str,
    end_date: str,
    previous_period_start: Optional[str] = None,
    project_ids: Optional[List[int]] = None,
    billable: Optional[bool] = None,
    rounding: Optional[int] = None,
    rounding_minutes: Optional[int] = None,
) -> str:
    """
    Get projects' data trends from a workspace.

    Parameters:
    - workspace_id: The ID of the workspace
    - start_date: Start date in YYYY-MM-DD format
    - end_date: End date in YYYY-MM-DD format
    - previous_period_start: Previous start date in YYYY-MM-DD format (optional)
    - project_ids: List of project IDs to filter by (optional)
    - billable: Whether to filter by billable projects (optional, premium feature)
    - rounding: Duration rounding settings (optional, premium feature)
    - rounding_minutes: Duration rounding minutes settings (optional, premium feature)

    Returns:
    Project trend data showing time spent in current and previous periods
    """
    url = f"{config.insights_api}/workspace/{workspace_id}/data_trends/projects"

    # Build request payload
    payload = {
        "start_date": start_date,
        "end_date": end_date,
    }

    # Add optional parameters
    if previous_period_start:
        payload["previous_period_start"] = previous_period_start
    if project_ids:
        payload["project_ids"] = project_ids
    if billable is not None:
        payload["billable"] = billable
    if rounding is not None:
        payload["rounding"] = rounding
    if rounding_minutes is not None:
        payload["rounding_minutes"] = rounding_minutes

    # Make POST request to insights API
    result = make_request("POST", url, data=payload)
    return json.dumps(result, indent=2)


@mcp.tool()
def get_profitability_insights(
    workspace_id: int,
    start_date: str,
    end_date: str,
    previous_period_start: Optional[str] = None,
    project_ids: Optional[List[int]] = None,
    billable: Optional[bool] = None,
    rounding: Optional[int] = None,
    rounding_minutes: Optional[int] = None,
) -> str:
    """
    Get profitability insights for projects in a workspace.

    Parameters:
    - workspace_id: The ID of the workspace
    - start_date: Start date in YYYY-MM-DD format
    - end_date: End date in YYYY-MM-DD format
    - previous_period_start: Previous start date in YYYY-MM-DD format (optional)
    - project_ids: List of project IDs to filter by (optional)
    - billable: Whether to filter by billable projects (optional, premium feature)
    - rounding: Duration rounding settings (optional, premium feature)
    - rounding_minutes: Duration rounding minutes settings (optional, premium feature)

    Returns:
    Profitability data showing revenue, costs, and profit margins for projects
    """
    url = f"{config.insights_api}/workspace/{workspace_id}/profitability/projects"

    # Build request payload
    payload = {
        "start_date": start_date,
        "end_date": end_date,
    }

    # Add optional parameters
    if previous_period_start:
        payload["previous_period_start"] = previous_period_start
    if project_ids:
        payload["project_ids"] = project_ids
    if billable is not None:
        payload["billable"] = billable
    if rounding is not None:
        payload["rounding"] = rounding
    if rounding_minutes is not None:
        payload["rounding_minutes"] = rounding_minutes

    # Make POST request to insights API
    result = make_request("POST", url, data=payload)
    return json.dumps(result, indent=2)


@mcp.tool()
def get_revenue_insights(
    workspace_id: int,
    start_date: str,
    end_date: str,
    previous_period_start: Optional[str] = None,
    project_ids: Optional[List[int]] = None,
    client_ids: Optional[List[int]] = None,
    billable: Optional[bool] = None,
    rounding: Optional[int] = None,
    rounding_minutes: Optional[int] = None,
) -> str:
    """
    Get revenue insights for projects in a workspace.

    Parameters:
    - workspace_id: The ID of the workspace
    - start_date: Start date in YYYY-MM-DD format
    - end_date: End date in YYYY-MM-DD format
    - previous_period_start: Previous start date in YYYY-MM-DD format (optional)
    - project_ids: List of project IDs to filter by (optional)
    - client_ids: List of client IDs to filter by (optional)
    - billable: Whether to filter by billable projects (optional, premium feature)
    - rounding: Duration rounding settings (optional, premium feature)
    - rounding_minutes: Duration rounding minutes settings (optional, premium feature)

    Returns:
    Revenue data showing billable amounts, hourly rates, and revenue trends
    """
    url = f"{config.insights_api}/workspace/{workspace_id}/revenue/summary"

    # Build request payload
    payload = {
        "start_date": start_date,
        "end_date": end_date,
    }

    # Add optional parameters
    if previous_period_start:
        payload["previous_period_start"] = previous_period_start
    if project_ids:
        payload["project_ids"] = project_ids
    if client_ids:
        payload["client_ids"] = client_ids
    if billable is not None:
        payload["billable"] = billable
    if rounding is not None:
        payload["rounding"] = rounding
    if rounding_minutes is not None:
        payload["rounding_minutes"] = rounding_minutes

    # Make POST request to insights API
    result = make_request("POST", url, data=payload)
    return json.dumps(result, indent=2)


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


@mcp.prompt()
def project_trends_analysis(workspace_id: int, start_date: str, end_date: str) -> str:
    """Create a prompt for analyzing project trends over time"""
    return f"""Please analyze the trends for projects in workspace {workspace_id} from {start_date} to {end_date}.
    
You can use the following tools:
- get_projects_data_trends(workspace_id={workspace_id}, start_date="{start_date}", end_date="{end_date}")
- get_profitability_insights(workspace_id={workspace_id}, start_date="{start_date}", end_date="{end_date}")
- get_revenue_insights(workspace_id={workspace_id}, start_date="{start_date}", end_date="{end_date}")

Please provide insights on:
1. Which projects are showing increased or decreased time allocation
2. Patterns in project usage over time
3. Recommendations for optimizing time allocation
4. Revenue analysis over time
5. Profitability analysis and margin trends
6. Suggestions for improving project profitability
"""


@mcp.prompt()
def profitability_analysis(workspace_id: int, start_date: str, end_date: str) -> str:
    """Create a prompt for analyzing project profitability"""
    return f"""Please analyze the profitability of projects in workspace {workspace_id} from {start_date} to {end_date}.
    
You can use the following tools:
- get_profitability_insights(workspace_id={workspace_id}, start_date="{start_date}", end_date="{end_date}")
- get_revenue_insights(workspace_id={workspace_id}, start_date="{start_date}", end_date="{end_date}")
- get_projects_data_trends(workspace_id={workspace_id}, start_date="{start_date}", end_date="{end_date}")

Please provide insights on:
1. Which projects are most and least profitable
2. Trends in profit margins over time
3. Correlation between time spent and profitability
4. Recommendations for improving overall profitability
5. Potential pricing adjustments for specific projects
6. Resource allocation optimization suggestions
"""


if __name__ == "__main__":
    mcp.run()
