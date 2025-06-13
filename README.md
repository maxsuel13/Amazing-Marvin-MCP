# 🚀 Amazing Marvin Model Context Provider

[![smithery badge](https://smithery.ai/badge/@bgheneti/amazing-marvin-mcp)](https://smithery.ai/server/@bgheneti/amazing-marvin-mcp)
[![PyPI version](https://badge.fury.io/py/amazing-marvin-mcp.svg)](https://badge.fury.io/py/amazing-marvin-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Model Context Protocol](https://img.shields.io/badge/MCP-Compatible-brightgreen.svg)](https://modelcontextprotocol.io/)

> 🤖 Supercharge your AI assistant with your Amazing Marvin productivity data

## 📋 Table of Contents

- [What is this?](#-what-is-this)
- [Quick Start (2 minutes)](#-quick-start-2-minutes)
- [What can you do with this?](#-what-can-you-do-with-this)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage Examples](#-usage-examples)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [Development](#-development)
- [Privacy & Security](#-privacy--security)

## 🎯 What is this?

The **Amazing Marvin MCP** bridges your [Amazing Marvin](https://amazingmarvin.com/) productivity system with AI assistants like Claude, Cursor, and others. Instead of manually copying your tasks and projects into chat, your AI can directly access and understand your productivity data.

### ✨ Key Benefits

- 🔄 **Real-time sync** - Your AI always sees your current tasks, projects, and categories
- 🧠 **Smart context** - AI understands your productivity patterns and priorities
- ⚡ **Instant access** - No more copy-pasting task lists or project details
- 🎯 **Focused assistance** - Get help with specific projects or overdue items
- 🛡️ **Secure** - Your data stays between Amazing Marvin and your AI client

## ⚡ Quick Start (2 minutes)

### Step 1: Get your Amazing Marvin API key
1. Open Amazing Marvin → Settings → API
2. Enable the API and copy your token
3. Keep this handy! 🔑

### Step 2: Install via Smithery (Recommended)
```bash
npx -y @smithery/cli install @bgheneti/amazing-marvin-mcp --client claude
```

### Step 3: Verify it's working
Ask your AI: *"What tasks do I have today?"*

🎉 **That's it!** Your AI can now see your Amazing Marvin data.

---

## 🛠️ What can you do with this?

This integration connects your Amazing Marvin data with AI assistants, helping you manage your productivity system more effectively. Here's what you can accomplish:

### 📋 Task Management
> *"What tasks are on my schedule today?"*
> *"What's due this week?"*
> *"Show me my high-priority tasks"*

### 🗂️ Project Organization
> *"Show me all tasks in my birthday scavenger hunt project"*
> *"What's the progress on my current projects?"*
> *"Help me organize these tasks into projects"*

### 🧠 Planning & Focus
> *"What should I focus on today based on my priorities?"*
> *"Plan my day based on my current deadlines and goals"*
> *"I'm feeling overwhelmed - help me identify my most important tasks"*

### ✅ Productivity Tracking
> *"How many tasks have I completed today?"*
> *"Show me my productivity for last week"*
> *"What did I accomplish on Tuesday?"*

### ⏱️ Time Management
> *"Start tracking time on my current task"*
> *"What am I currently tracking time on?"*
> *"Stop tracking time on this task"*

The integration provides actual data from your Amazing Marvin account, allowing your AI assistant to give personalized productivity advice rather than generic suggestions.

**Limitations:** While this covers most core features, some advanced Amazing Marvin capabilities like strategies, customizations, and reward systems have limited API support.

## 📦 Installation

### Option 1: Smithery (Easiest)
```bash
npx -y @smithery/cli install @bgheneti/amazing-marvin-mcp --client claude
```
[Visit Smithery Registry](https://smithery.ai/server/@bgheneti/amazing-marvin-mcp) for other clients.

### Option 2: Manual Installation

#### Prerequisites
- ✅ Python 3.8+
- ✅ Claude Desktop, Cursor, Windsurf, or another MCP client
- ✅ Amazing Marvin account with API access

#### Via pip
```bash
pip install amazing-marvin-mcp
```

#### From source
```bash
git clone https://github.com/bgheneti/Amazing-Marvin-MCP.git
cd Amazing-Marvin-MCP
pip install -e .
```

#### 📱 Client Configuration

<details>
<summary>🖥️ Claude Desktop</summary>

Add to your `claude_desktop_config.json`:

**📍 Config file locations:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

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
<summary>🎯 Cursor</summary>

Add to your MCP settings:

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
<summary>💨 Windsurf</summary>

Add to your Windsurf MCP configuration:

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

## 💡 Usage Examples

The MCP provides specific tools that your AI can use. Simply ask your AI to help with productivity tasks and it will use the appropriate tools:

| What you might ask | Tools the AI will use |
|-------------------|----------------------|
| *"What tasks do I have today?"* | `get_tasks()` |
| *"Show me my projects"* | `get_projects()` |
| *"What's overdue?"* | `get_due_items()` |
| *"Create a new task for X"* | `create_task()` |
| *"Mark task Y as done"* | `mark_task_done()` |
| *"Start tracking time on this"* | `start_time_tracking()` |

### 🎯 Understanding Your Default Setup

Amazing Marvin creates these default containers for most users:

- **📁 Work** - Professional/job tasks
- **🏠 Personal** - Personal life tasks
- **📥 Inbox** - Uncategorized items waiting to be sorted

Your AI understands this structure and can help organize tasks accordingly.

## 🔧 Troubleshooting

### ❌ Common Issues

<details>
<summary><strong>"API key not found" error</strong></summary>

**Problem**: The MCP can't find your API key.

**Solutions**:
1. Verify your API key is correct in Amazing Marvin Settings → API
2. Check the environment variable: `echo $AMAZING_MARVIN_API_KEY`
3. Restart your AI client after setting the key
4. Ensure no extra spaces in your API key
</details>

<details>
<summary><strong>"Connection refused" or timeout errors</strong></summary>

**Problem**: Can't connect to Amazing Marvin API.

**Solutions**:
1. Check your internet connection
2. Verify Amazing Marvin service status
3. Try the connection test: `python -c "import requests; print(requests.get('https://serv.amazingmarvin.com/api').status_code)"`
4. Check if you're behind a corporate firewall
</details>

<details>
<summary><strong>AI says "I don't see any Amazing Marvin data"</strong></summary>

**Problem**: MCP is running but not returning data.

**Solutions**:
1. Ask explicitly: *"Use the Amazing Marvin tool to get my tasks"*
2. Check if you have any tasks in Amazing Marvin
3. Verify API permissions in Amazing Marvin settings
4. Restart your AI client
</details>

<details>
<summary><strong>Python module not found</strong></summary>

**Problem**: `ModuleNotFoundError: No module named 'amazing_marvin_mcp'`

**Solutions**:
1. Reinstall: `pip install --force-reinstall amazing-marvin-mcp`
2. Check Python path: `python -c "import sys; print(sys.path)"`
3. Use full path: `which python` and use that in your config
</details>

## ❓ FAQ

<details>
<summary><strong>Is my data secure?</strong></summary>

Yes! Your data flows directly between Amazing Marvin and your AI client. The MCP server runs locally on your machine and doesn't store or transmit your data elsewhere.
</details>

<details>
<summary><strong>Does this work with all AI assistants?</strong></summary>

It works with any AI client that supports the Model Context Protocol (MCP), including Claude Desktop, Cursor, Windsurf, and others.
</details>

<details>
<summary><strong>What Amazing Marvin data can the AI access?</strong></summary>

The AI can access:
- ✅ Tasks and subtasks
- ✅ Projects and categories
- ✅ Due dates and priorities
- ✅ Task status (completed/pending)
- ✅ Time tracking data and current tracking status
- ✅ Goals, labels, and account information
- ✅ Completed tasks and productivity analytics
</details>

<details>
<summary><strong>Will this slow down my AI assistant?</strong></summary>

The MCP makes fresh API calls to Amazing Marvin for each request. Response times depend on Amazing Marvin's API performance and your internet connection. Data is fetched in real-time when you ask productivity-related questions.
</details>

<details>
<summary><strong>Can the AI modify my Amazing Marvin data?</strong></summary>

Yes, the AI can both read and write to your Amazing Marvin account. It can:
- ✅ Create new tasks and projects
- ✅ Mark tasks as complete
- ✅ Start and stop time tracking
- ✅ Create batch operations
- ✅ Claim reward points

Be mindful when asking the AI to make changes to your data.
</details>

<details>
<summary><strong>Can I see completed tasks?</strong></summary>

Yes! The MCP can find and display completed tasks in several ways:

**📊 In Daily Focus View:**
- ✅ Shows today's completed tasks alongside pending ones
- ✅ Includes completion count and productivity notes
- ✅ Separates completed from pending for clear progress tracking

**📁 In Project Overviews:**
- ✅ Lists completed vs pending tasks separately
- ✅ Shows completion rate and progress summary
- ✅ Provides detailed task breakdowns

**🔍 Efficient Historical Access:**
- ✅ Get completed tasks for any specific date (e.g., "June 10th")
- ✅ Flexible time range summaries (1 day, 7 days, 30 days, or custom date ranges)
- ✅ **Complete task data included** - no additional API calls needed for task details
- ✅ **Smart caching** - historical data cached for 10 minutes to avoid redundant calls
- ✅ Project-wise completion analytics with resolved project names
- ✅ Efficient API filtering with cache hit rate tracking
- ✅ Real-time access to completion timestamps and project correlations
</details>

<details>
<summary><strong>What can't the MCP do?</strong></summary>

**🚫 Cannot Delete or Remove:**
- ❌ Delete tasks (requires special API permissions)
- ❌ Delete projects or categories
- ❌ Remove labels or goals
- ❌ Clear time tracking history

**📝 Cannot Edit:**
- ❌ Modify existing task content (title, notes, due dates)
- ❌ Move tasks between projects
- ❌ Change task priorities or labels
- ❌ Update project settings

**📚 Limited Access:**
- ❌ Full historical completed task archive
- ❌ Detailed time tracking reports (only basic tracking)
- ❌ Private notes or sensitive data
- ❌ Advanced Amazing Marvin features (strategies, rewards setup)

For these operations, use the Amazing Marvin app directly.
</details>

<details>
<summary><strong>How often is the data updated?</strong></summary>

Data is fetched in real-time with each request to Amazing Marvin's API. There's no background syncing or caching - you always get the most current data from your Amazing Marvin account.
</details>

## 👨‍💻 Development

### 🛠️ Setup
```bash
git clone https://github.com/bgheneti/Amazing-Marvin-MCP.git
cd Amazing-Marvin-MCP
pip install -e ".[dev]"
pre-commit install
```

### 🔑 Set your API key

**Option A: Environment variable**
```bash
export AMAZING_MARVIN_API_KEY="your-api-key-here"
```

**Option B: Create a `.env` file**
```env
AMAZING_MARVIN_API_KEY=your-api-key-here
```

### 🧪 Testing
```bash
pytest tests/ -v
```

**⚠️ Note**: Tests create temporary items in your Amazing Marvin account with `[TEST]` prefixes. These may need manual cleanup due to API limitations.

### 📋 Code Quality
```bash
# Run all checks
pre-commit run --all-files

# Individual tools
ruff check .          # Linting
ruff format .         # Formatting
mypy .               # Type checking
pytest tests/        # Tests
```

### 🔄 Available Tools
The MCP provides 27 comprehensive tools to AI assistants:

**📖 Read Operations:**
- `get_tasks()` - Today's scheduled items
- `get_projects()` - All projects
- `get_categories()` - All categories
- `get_due_items()` - Overdue/due items
- `get_child_tasks()` - Subtasks
- `get_labels()` - Task labels
- `get_goals()` - Goals and objectives
- `get_account_info()` - Account details
- `get_completed_tasks()` - Completed items with date categorization
- `get_completed_tasks_for_date()` - Completed items for specific date
- `get_productivity_summary_for_time_range()` - Flexible productivity analytics (by days, or start/end dates)
- `get_currently_tracked_item()` - Active time tracking

**✏️ Write Operations:**
- `create_task()` - Create new tasks
- `mark_task_done()` - Complete tasks
- `create_project()` - Create new projects
- `start_time_tracking()` - Begin time tracking
- `stop_time_tracking()` - End time tracking
- `batch_mark_done()` - Complete multiple tasks
- `batch_create_tasks()` - Create multiple tasks
- `claim_reward_points()` - Claim kudos points

**🔧 Utility Operations:**
- `test_api_connection()` - Verify API connectivity
- `get_project_overview()` - Project analytics
- `get_daily_focus()` - Daily priorities
- `get_productivity_summary()` - Performance metrics
- `time_tracking_summary()` - Time analytics
- `quick_daily_planning()` - Planning assistance
- `create_project_with_tasks()` - Project setup
- `get_time_tracks()` - Time tracking history

## 🔒 Privacy & Security

### 🛡️ Your Data Protection
- **Local Processing**: MCP runs entirely on your machine
- **Direct Connection**: Data goes directly from Amazing Marvin to your AI
- **No Cloud Storage**: Nothing is stored on external servers
- **API Key Security**: Store your key securely using environment variables

### 🔐 Best Practices
- ✅ Use environment variables for API keys (not config files)
- ✅ Don't share your API key in screenshots or logs
- ✅ Keep your API key secure and treat it like a password

### ⚖️ API Limitations & Rate Limiting

**Rate Limiting:**
- Amazing Marvin API has rate limits on requests per minute
- The MCP makes API calls as needed for each request
- Historical data is cached for 10 minutes to reduce API load
- Rate limit errors (429) may occur with frequent requests

**API Endpoint Characteristics:**
- `/doneItems`: Provides completed tasks, can be filtered by date
- `/todayItems`: Returns scheduled tasks for the current day
- `/children`: Returns tasks belonging to a specific parent/project
- `/categories`: Returns projects and categories
- Data must be fetched through specific endpoints - no bulk data export

**Performance Optimization:**
- Historical data is cached for 10 minutes (except today's data)
- Multiple API calls may be required for comprehensive queries
- Batch operations are available for task creation and completion
- Cache is cleared after 1 hour of inactivity

## 📄 License

MIT License - see [LICENSE](https://opensource.org/licenses/MIT) for details.

---

<div align="center">

**Developed for Amazing Marvin users**

[Report Issues](https://github.com/bgheneti/Amazing-Marvin-MCP/issues) • [Request Features](https://github.com/bgheneti/Amazing-Marvin-MCP/issues/new) • [Star on GitHub](https://github.com/bgheneti/Amazing-Marvin-MCP)

</div>
