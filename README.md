# Toggl MCP Server

A Model Context Protocol (MCP) server for interacting with the Toggl API. This MCP server enables you to seamlessly work with Toggl's APIs through Claude or other LLMs.

## Overview

This project implements an MCP server using the official [Model Context Protocol Python SDK](https://github.com/modelcontextprotocol/python-sdk) that provides read-only access to the Toggl API. It allows Claude and other LLMs to interact with your Toggl data, analyze time entries, generate reports, and provide insights on your time tracking.

## Features

- Read access to Toggl APIs through a unified interface
- Authentication handled automatically with your Toggl API key
- Structured data models for Toggl entities
- Support for read operations:
  - Time entries retrieval
  - Projects, clients, tasks, and tags information
  - Workspace information and settings
  - Reports generation (weekly, detailed, summary)
  - Webhook subscription information
  - Project trends and insights analysis

## Setup

### Prerequisites

- Python 3.10 or higher
- UV package manager
- A Toggl account with an API key

### Environment Variables

Set the following environment variable:

```bash
TOGGL_API_KEY=your_toggl_api_key
```

You can find your API key in your Toggl profile settings. The easiest way to set this up is to create a `.env` file in the project root with this variable.

### Installation with UV

1. Install UV:

```bash
pip install uv
```

2. Create a virtual environment and install dependencies:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

3. Install the MCP server in Claude Desktop:

```bash
mcp install toggl_mcp_server.py
```

### Development Mode

For testing and development:

```bash
mcp dev toggl_mcp_server.py
```

This will launch the MCP Inspector where you can test your tools and resources interactively.

### Docker (optional)

If you prefer using Docker:

```bash
docker build -t toggl-mcp .
docker run -e TOGGL_API_KEY=your_toggl_api_key toggl-mcp
```

## Usage

Once installed in Claude Desktop, you can interact with the Toggl API through Claude. Here are some examples:

### Basic Queries

1. Ask Claude to analyze your time entries:

   ```
   Can you analyze my time entries for workspace 12345?
   ```

2. Get information about a specific project:

   ```
   Tell me about project 67890
   ```

3. Generate reports:
   ```
   Create a weekly report for workspace 12345 for the last month
   ```

### Advanced Queries

1. Analyze productivity patterns:

   ```
   Can you analyze my time entries for workspace 12345 and tell me when I'm most productive during the day?
   ```

2. Compare project time allocation:

   ```
   Compare the time spent on projects A and B in workspace 12345 over the last quarter
   ```

3. Find gaps in time tracking:
   ```
   Identify days where I have less than 8 hours tracked in workspace 12345 in the last two weeks
   ```

### Insights Queries

1. Analyze project trends:

   ```
   Analyze the trends for projects in workspace 12345 from 2023-01-01 to 2023-03-31
   ```

2. Compare current and previous periods:

   ```
   Compare project time allocation between this month and last month for workspace 12345
   ```

3. Identify growing or declining projects:
   ```
   Which projects in workspace 12345 have shown the most growth in time allocation over the last quarter?
   ```

### Profitability Queries

1. Analyze project profitability:

   ```
   Analyze the profitability of projects in workspace 12345 from 2023-01-01 to 2023-03-31
   ```

2. Find most profitable projects:

   ```
   Which projects in workspace 12345 have the highest profit margins?
   ```

3. Optimize resource allocation:
   ```
   How can I improve the profitability of projects in workspace 12345?
   ```

## Resources

The server exposes the following resources:

- `me://` - Current user data
- `workspaces://` - All workspaces
- `workspaces://{workspace_id}` - Specific workspace
- `workspaces://{workspace_id}/users` - Users in a workspace
- `workspaces://{workspace_id}/clients` - Clients in a workspace
- `workspaces://{workspace_id}/projects` - Projects in a workspace
- `workspaces://{workspace_id}/tasks` - Tasks in a workspace
- `workspaces://{workspace_id}/tags` - Tags in a workspace
- `time_entries://{time_entry_id}` - Specific time entry
- `time-entries:/current` - Currently running time entry
- `projects://{project_id}` - Specific project
- `clients://{client_id}` - Specific client
- `tags://{tag_id}` - Specific tag
- `tasks://{task_id}` - Specific task

## Tools

The server provides the following tools:

- `get_weekly_report` - Generate a weekly report
- `get_detailed_report` - Generate a detailed report
- `get_summary_report` - Generate a summary report
- `get_webhook_subscriptions` - List webhook subscriptions
- `get_projects_data_trends` - Get project trend data over time
- `get_profitability_insights` - Get project profitability data
- `get_revenue_insights` - Get revenue data and trends

## Prompts

The server includes these prompt templates:

- `analyze_time_entries` - Analyze time entries for a workspace
- `project_analysis` - Analyze a specific project
- `project_trends_analysis` - Analyze project trends over time
- `profitability_analysis` - Analyze project profitability

## How It Works

This project uses the official [Model Context Protocol Python SDK](https://github.com/modelcontextprotocol/python-sdk) to build an MCP server that exposes resources and tools that Claude can use to interact with the Toggl API.

When you ask Claude a question about your Toggl data, it can:

1. Access resources like workspaces, projects, and time entries
2. Use tools to generate reports and analyze data
3. Provide insights and visualizations based on your data

All API calls are authenticated using your Toggl API key, and the server only provides read access to your data.

## Rate Limiting

Be mindful of Toggl's rate limiting policies:

- Track API: 1 request per second (per IP per API key)
- Reports API: 1 request per second (per IP per API key)

## Troubleshooting

If you encounter issues:

1. Verify your API key is correct
2. Check that you have the necessary permissions in Toggl
3. Ensure you're using Python 3.10 or higher
4. Try running in development mode to debug: `mcp dev toggl_mcp_server.py`
5. Test your API key directly with curl:
   ```bash
   curl -v -u your_api_key:api_token -X GET https://api.track.toggl.com/api/v9/me
   ```

## License

MIT

## Acknowledgements

This project uses:

- [Model Context Protocol Python SDK](https://github.com/modelcontextprotocol/python-sdk) for building the MCP server
- [Toggl API](https://github.com/toggl/toggl_api_docs) for time tracking data
- [Toggl Insights API](https://engineering.toggl.com/docs/reports/insights/) for project trend analysis
