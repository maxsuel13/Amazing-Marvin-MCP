# Amazing Marvin Model Context Provider

[![smithery badge](https://smithery.ai/badge/@bgheneti/amazing-marvin-mcp)](https://smithery.ai/server/@bgheneti/amazing-marvin-mcp)
[![PyPI version](https://badge.fury.io/py/amazing-marvin-mcp.svg)](https://badge.fury.io/py/amazing-marvin-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Model Context Protocol](https://img.shields.io/badge/MCP-Compatible-brightgreen.svg)](https://modelcontextprotocol.io/)

This is a Model Context Provider for [Amazing Marvin](https://amazingmarvin.com/) that provides your tasks, projects, categories, and other data from your Marvin account to AI models.

## Features

- Connects to Amazing Marvin API to fetch your productivity data
- Uses Server-Sent Events (SSE) transport for efficient data streaming
- Easy to install and configure
- Compatible with AI assistants that support context providers

## Prerequisites

### Installing via Smithery

To install amazing-marvin-mcp for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@bgheneti/amazing-marvin-mcp):

```bash
npx -y @smithery/cli install @bgheneti/amazing-marvin-mcp --client claude
```

### Requirements
- Python >= 3.8
- Cursor, Windsurf, Claude Desktop or another MCP Client
- Amazing Marvin account with API access

### Getting Your API Key

You'll need an API key from Amazing Marvin to use this MCP:

1. Go to Settings in Amazing Marvin
2. Navigate to the API section
3. Enable the API and copy your API token

## Installation

### Using Smithery (Recommended)

You can easily install this MCP with [Smithery](https://smithery.ai/):

```bash
smithery install @bgheneti/amazing-marvin-mcp
```

Or visit the [Smithery registry page](https://smithery.ai/server/@bgheneti/amazing-marvin-mcp) for more installation options.

### Manual Installation

<details>
<summary><strong>Claude Desktop Configuration</strong></summary>

Add this to your `claude_desktop_config.json`:

```json
{
 "mcpServers": {
   "amazing-marvin": {
     "command": "python",
     "args": ["-m", "amazing_marvin_mcp"],
     "env": {
       "AMAZING_MARVIN_API_KEY": "your-api-key-here"
     }
   }
 }
}
```
</details>

<details>
<summary><strong>Cursor Configuration</strong></summary>

Add this to your MCP settings:

```json
{
 "mcpServers": {
   "amazing-marvin": {
     "command": "python",
     "args": ["-m", "amazing_marvin_mcp"],
     "env": {
       "AMAZING_MARVIN_API_KEY": "your-api-key-here"
     }
   }
 }
}
```
</details>

<details>
<summary><strong>VS Code Configuration</strong></summary>

Add this to your VS Code MCP settings:

```json
{
 "mcpServers": {
   "amazing-marvin": {
     "command": "python",
     "args": ["-m", "amazing_marvin_mcp"],
     "env": {
       "AMAZING_MARVIN_API_KEY": "your-api-key-here"
     }
   }
 }
}
```
</details>

#### Using pip

```bash
pip install amazing-marvin-mcp
```

#### From Source

```bash
git clone https://github.com/bgheneti/Amazing-Marvin-MCP.git
cd Amazing-Marvin-MCP
pip install -e .
```

## Configuration

Set your API key as an environment variable:

```bash
export AMAZING_MARVIN_API_KEY="your-api-key"
```

Alternatively, create a `.env` file in the project root:

```
AMAZING_MARVIN_API_KEY=your-api-key
```

## Usage

### Starting the server

```bash
amazing-marvin-mcp
```

This will start the server on port 3000 by default. You can customize the port by setting the `PORT` environment variable.

### Querying for context

The MCP will respond to different query types:
- Tasks/todos: Any query containing "task" or "todo"  
- Projects: Any query containing "project"
- Categories: Any query containing "category" or "categor"
- Specific dates: Any query containing a date in YYYY-MM-DD format
- All data: Any query containing "all"

If no specific context is requested, it will default to returning your tasks.

## Default Projects and Inbox

When you connect your Amazing Marvin account, the MCP will recognize **Work** and **Personal** as default projects that are automatically created for most users. These help you organize your tasks into common categories right from the start.  
Additionally, the **Inbox** serves as a special area for capturing uncategorized tasks before you sort them into projects.

- **Work**: Default project for professional or job-related tasks.
- **Personal**: Default project for personal or non-work tasks.
- **Inbox**: Special holding area for new or uncategorized tasks.

You can rename, remove, or add more projects as needed.

## Development

### Setup

```bash
git clone https://github.com/bgheneti/Amazing-Marvin-MCP.git
cd Amazing-Marvin-MCP
pip install -e ".[dev]"
```

### Environment Variables

Set your API key for development:

```bash
export AMAZING_MARVIN_API_KEY="your-api-key"
```

### Testing

To test your API connection and fetch your projects:

```bash
python api_test.py --api-key "your-api-key" --test-projects
```

This will verify that your projects (including default ones) are accessible via the MCP.

## License

MIT
