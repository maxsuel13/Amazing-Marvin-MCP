import logging
from typing import Any, Dict, Optional

from fastmcp import FastMCP

from .api import MarvinAPIClient
from .config import get_settings

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize MCP
mcp = FastMCP(name="amazing-marvin-mcp")


@mcp.tool()
async def get_tasks() -> Dict[str, Any]:
    """Get tasks from Amazing Marvin"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)
    return {"tasks": api_client.get_tasks()}


@mcp.tool()
async def get_projects() -> Dict[str, Any]:
    """Get projects from Amazing Marvin"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)
    return {"projects": api_client.get_projects()}


@mcp.tool()
async def get_categories() -> Dict[str, Any]:
    """Get categories from Amazing Marvin"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)
    return {"categories": api_client.get_categories()}


@mcp.tool()
async def get_due_items() -> Dict[str, Any]:
    """Get all due items from Amazing Marvin"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)
    return {"due_items": api_client.get_due_items()}


@mcp.tool()
async def get_child_tasks(parent_id: str) -> Dict[str, Any]:
    """Get child tasks of a specific parent task or project (experimental)"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)
    return {"children": api_client.get_children(parent_id), "parent_id": parent_id}


@mcp.tool()
async def get_labels() -> Dict[str, Any]:
    """Get all labels from Amazing Marvin"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)
    return {"labels": api_client.get_labels()}


@mcp.tool()
async def get_goals() -> Dict[str, Any]:
    """Get all goals from Amazing Marvin"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)
    return {"goals": api_client.get_goals()}


@mcp.tool()
async def get_account_info() -> Dict[str, Any]:
    """Get account information from Amazing Marvin"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)
    return {"account": api_client.get_account_info()}


@mcp.tool()
async def get_currently_tracked_item() -> Dict[str, Any]:
    """Get currently tracked item from Amazing Marvin"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)
    return {"tracked_item": api_client.get_currently_tracked_item()}


@mcp.tool()
async def create_task(
    title: str,
    project_id: Optional[str] = None,
    category_id: Optional[str] = None,
    due_date: Optional[str] = None,
    note: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new task in Amazing Marvin"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)

    task_data = {"title": title}
    if project_id:
        task_data["parentId"] = project_id
    if category_id:
        task_data["categoryId"] = category_id
    if due_date:
        task_data["dueDate"] = due_date
    if note:
        task_data["note"] = note

    return {"created_task": api_client.create_task(task_data)}


@mcp.tool()
async def mark_task_done(item_id: str, timezone_offset: int = 0) -> Dict[str, Any]:
    """Mark a task as completed in Amazing Marvin"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)
    return {"completed_task": api_client.mark_task_done(item_id, timezone_offset)}


@mcp.tool()
async def test_api_connection() -> Dict[str, Any]:
    """Test the API connection and credentials"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)
    return {"status": api_client.test_api_connection()}


@mcp.tool()
async def start_time_tracking(task_id: str) -> Dict[str, Any]:
    """Start time tracking for a specific task"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)
    return {"tracking": api_client.start_time_tracking(task_id)}


@mcp.tool()
async def stop_time_tracking(task_id: str) -> Dict[str, Any]:
    """Stop time tracking for a specific task"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)
    return {"tracking": api_client.stop_time_tracking(task_id)}


@mcp.tool()
async def get_time_tracks(task_ids: list) -> Dict[str, Any]:
    """Get time tracking data for specific tasks"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)
    return {"time_tracks": api_client.get_time_tracks(task_ids)}


@mcp.tool()
async def claim_reward_points(points: int, item_id: str, date: str) -> Dict[str, Any]:
    """Claim reward points for completing a task"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)
    return {"reward": api_client.claim_reward_points(points, item_id, date)}


@mcp.tool()
async def get_kudos_info() -> Dict[str, Any]:
    """Get kudos and achievement information"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)
    return {"kudos": api_client.get_kudos_info()}


@mcp.tool()
async def create_project(title: str, project_type: str = "project") -> Dict[str, Any]:
    """Create a new project in Amazing Marvin"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)

    project_data = {"title": title, "type": project_type}
    return {"created_project": api_client.create_project(project_data)}


@mcp.tool()
async def create_project_with_tasks(
    project_title: str, task_titles: list, project_type: str = "project"
) -> Dict[str, Any]:
    """Create a project with multiple tasks at once"""
    from .utils import create_project_with_tasks_util

    return create_project_with_tasks_util(project_title, task_titles, project_type)


@mcp.tool()
async def get_project_overview(project_id: str) -> Dict[str, Any]:
    """Get comprehensive overview of a project including tasks and progress"""
    from .utils import get_project_overview_util

    return get_project_overview_util(project_id)


@mcp.tool()
async def get_daily_focus() -> Dict[str, Any]:
    """Get today's focus items - due items and scheduled tasks"""
    from .utils import get_daily_focus_util

    return get_daily_focus_util()


@mcp.tool()
async def get_productivity_summary() -> Dict[str, Any]:
    """Get productivity summary with completed tasks and goals progress"""
    from .utils import get_productivity_summary_util

    return get_productivity_summary_util()


@mcp.tool()
async def batch_create_tasks(
    task_list: list, project_id: Optional[str] = None, category_id: Optional[str] = None
) -> Dict[str, Any]:
    """Create multiple tasks at once with optional project/category assignment"""
    from .utils import batch_create_tasks_util

    return batch_create_tasks_util(task_list, project_id, category_id)


@mcp.tool()
async def batch_mark_done(task_ids: list) -> Dict[str, Any]:
    """Mark multiple tasks as done at once"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)

    completed_tasks = []
    failed_tasks = []

    for task_id in task_ids:
        try:
            completed_task = api_client.mark_task_done(task_id)
            completed_tasks.append(completed_task)
        except Exception as e:
            failed_tasks.append({"task_id": task_id, "error": str(e)})

    return {
        "completed_tasks": completed_tasks,
        "failed_tasks": failed_tasks,
        "success_count": len(completed_tasks),
        "failure_count": len(failed_tasks),
        "total_requested": len(task_ids),
    }


@mcp.tool()
async def quick_daily_planning() -> Dict[str, Any]:
    """Get a quick daily planning overview with actionable insights"""
    from .utils import quick_daily_planning_util

    return quick_daily_planning_util()


@mcp.tool()
async def time_tracking_summary() -> Dict[str, Any]:
    """Get time tracking overview and productivity insights"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)

    # Get currently tracked item
    tracked_item = api_client.get_currently_tracked_item()

    # Get account info which may include time tracking stats
    account = api_client.get_account_info()

    # Get kudos info for productivity rewards
    kudos = api_client.get_kudos_info()

    is_tracking = tracked_item and "message" not in tracked_item

    return {
        "currently_tracking": is_tracking,
        "tracked_item": tracked_item if is_tracking else None,
        "account_stats": account,
        "kudos_info": kudos,
        "tracking_status": "Active" if is_tracking else "Not tracking",
        "suggestion": "Start tracking a task to measure productivity"
        if not is_tracking
        else f"Currently tracking: {tracked_item.get('title', 'Unknown task')}",
    }


@mcp.tool()
async def get_completed_tasks() -> Dict[str, Any]:
    """Get completed tasks from available sources

    Note: Due to API limitations, this searches multiple endpoints and filters for completed tasks.
    May not include all historical completed tasks. For comprehensive history, use the Amazing Marvin app directly.
    """
    from .utils import get_completed_tasks_util

    return get_completed_tasks_util()


def start():
    """Start the MCP server"""
    mcp.run()


if __name__ == "__main__":
    start()
