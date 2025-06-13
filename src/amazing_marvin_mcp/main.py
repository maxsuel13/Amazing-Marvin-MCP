import logging
from typing import Any

from fastmcp import FastMCP

from .api import create_api_client

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize MCP
mcp: FastMCP = FastMCP(name="amazing-marvin-mcp")


@mcp.tool()
async def get_tasks() -> dict[str, Any]:
    """Get tasks from Amazing Marvin"""
    api_client = create_api_client()
    return {"tasks": api_client.get_tasks()}


@mcp.tool()
async def get_projects() -> dict[str, Any]:
    """Get projects from Amazing Marvin"""
    api_client = create_api_client()
    return {"projects": api_client.get_projects()}


@mcp.tool()
async def get_categories() -> dict[str, Any]:
    """Get categories from Amazing Marvin"""
    api_client = create_api_client()
    return {"categories": api_client.get_categories()}


@mcp.tool()
async def get_due_items() -> dict[str, Any]:
    """Get all due items from Amazing Marvin"""
    api_client = create_api_client()
    return {"due_items": api_client.get_due_items()}


@mcp.tool()
async def get_child_tasks(parent_id: str) -> dict[str, Any]:
    """Get child tasks of a specific parent task or project (experimental)"""
    api_client = create_api_client()
    return {"children": api_client.get_children(parent_id), "parent_id": parent_id}


@mcp.tool()
async def get_labels() -> dict[str, Any]:
    """Get all labels from Amazing Marvin"""
    api_client = create_api_client()
    return {"labels": api_client.get_labels()}


@mcp.tool()
async def get_goals() -> dict[str, Any]:
    """Get all goals from Amazing Marvin"""
    api_client = create_api_client()
    return {"goals": api_client.get_goals()}


@mcp.tool()
async def get_account_info() -> dict[str, Any]:
    """Get account information from Amazing Marvin"""
    api_client = create_api_client()
    return {"account": api_client.get_account_info()}


@mcp.tool()
async def get_currently_tracked_item() -> dict[str, Any]:
    """Get currently tracked item from Amazing Marvin"""
    api_client = create_api_client()
    return {"tracked_item": api_client.get_currently_tracked_item()}


@mcp.tool()
async def create_task(
    title: str,
    project_id: str | None = None,
    category_id: str | None = None,
    due_date: str | None = None,
    note: str | None = None,
) -> dict[str, Any]:
    """Create a new task in Amazing Marvin"""
    api_client = create_api_client()

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
async def mark_task_done(item_id: str, timezone_offset: int = 0) -> dict[str, Any]:
    """Mark a task as completed in Amazing Marvin"""
    api_client = create_api_client()
    return {"completed_task": api_client.mark_task_done(item_id, timezone_offset)}


@mcp.tool()
async def test_api_connection() -> dict[str, Any]:
    """Test the API connection and credentials"""
    api_client = create_api_client()
    return {"status": api_client.test_api_connection()}


@mcp.tool()
async def start_time_tracking(task_id: str) -> dict[str, Any]:
    """Start time tracking for a specific task"""
    api_client = create_api_client()
    return {"tracking": api_client.start_time_tracking(task_id)}


@mcp.tool()
async def stop_time_tracking(task_id: str) -> dict[str, Any]:
    """Stop time tracking for a specific task"""
    api_client = create_api_client()
    return {"tracking": api_client.stop_time_tracking(task_id)}


@mcp.tool()
async def get_time_tracks(task_ids: list[str]) -> dict[str, Any]:
    """Get time tracking data for specific tasks"""
    api_client = create_api_client()
    return {"time_tracks": api_client.get_time_tracks(task_ids)}


@mcp.tool()
async def claim_reward_points(points: int, item_id: str, date: str) -> dict[str, Any]:
    """Claim reward points for completing a task"""
    api_client = create_api_client()
    return {"reward": api_client.claim_reward_points(points, item_id, date)}


@mcp.tool()
async def get_kudos_info() -> dict[str, Any]:
    """Get kudos and achievement information"""
    api_client = create_api_client()
    return {"kudos": api_client.get_kudos_info()}


@mcp.tool()
async def create_project(title: str, project_type: str = "project") -> dict[str, Any]:
    """Create a new project in Amazing Marvin"""
    api_client = create_api_client()

    project_data = {"title": title, "type": project_type}
    return {"created_project": api_client.create_project(project_data)}


@mcp.tool()
async def create_project_with_tasks(
    project_title: str, task_titles: list[str], project_type: str = "project"
) -> dict[str, Any]:
    """Create a project with multiple tasks at once"""
    from .projects import create_project_with_tasks as create_project_impl

    api_client = create_api_client()
    return create_project_impl(api_client, project_title, task_titles, project_type)


@mcp.tool()
async def get_project_overview(project_id: str) -> dict[str, Any]:
    """Get comprehensive overview of a project including tasks and progress"""
    from .projects import get_project_overview as get_project_overview_impl

    api_client = create_api_client()
    return get_project_overview_impl(api_client, project_id)


@mcp.tool()
async def get_daily_focus() -> dict[str, Any]:
    """Get today's focus items - due items and scheduled tasks"""
    from .tasks import get_daily_focus as get_daily_focus_impl

    api_client = create_api_client()
    return get_daily_focus_impl(api_client)


@mcp.tool()
async def get_productivity_summary() -> dict[str, Any]:
    """Get productivity summary with completed tasks and goals progress"""
    from .analytics import get_productivity_summary as get_productivity_summary_impl

    api_client = create_api_client()
    return get_productivity_summary_impl(api_client)


@mcp.tool()
async def batch_create_tasks(
    task_list: list[str],
    project_id: str | None = None,
    category_id: str | None = None,
) -> dict[str, Any]:
    """Create multiple tasks at once with optional project/category assignment"""
    from .tasks import batch_create_tasks as batch_create_tasks_impl

    api_client = create_api_client()
    return batch_create_tasks_impl(api_client, task_list, project_id, category_id)


@mcp.tool()
async def batch_mark_done(task_ids: list[str]) -> dict[str, Any]:
    """Mark multiple tasks as done at once"""
    api_client = create_api_client()

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
async def quick_daily_planning() -> dict[str, Any]:
    """Get a quick daily planning overview with actionable insights"""
    from .tasks import quick_daily_planning as quick_daily_planning_impl

    api_client = create_api_client()
    return quick_daily_planning_impl(api_client)


@mcp.tool()
async def time_tracking_summary() -> dict[str, Any]:
    """Get time tracking overview and productivity insights"""
    api_client = create_api_client()

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
async def get_completed_tasks() -> dict[str, Any]:
    """Get completed tasks with efficient date filtering and categorization"""
    from .analytics import get_completed_tasks as get_completed_tasks_impl

    api_client = create_api_client()
    return get_completed_tasks_impl(api_client)


@mcp.tool()
async def get_productivity_summary_for_time_range(
    days: int | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> dict[str, Any]:
    """Get a comprehensive productivity summary for a specified time range

    Args:
        days: Number of days to analyze from today backwards (default: 7 for weekly summary)
              Examples: 1 (today only), 7 (past week), 30 (past month)
        start_date: Start date in YYYY-MM-DD format (overrides days parameter)
        end_date: End date in YYYY-MM-DD format (defaults to today if start_date provided)

    Examples:
        - get_productivity_summary_for_time_range(days=30)  # Past 30 days
        - get_productivity_summary_for_time_range(start_date='2025-06-01', end_date='2025-06-10')
        - get_productivity_summary_for_time_range(start_date='2025-06-01')  # June 1st to today
    """
    from .analytics import (
        get_productivity_summary_for_time_range as get_productivity_summary_for_time_range_impl,
    )

    api_client = create_api_client()
    return get_productivity_summary_for_time_range_impl(
        api_client, days, start_date, end_date
    )


@mcp.tool()
async def get_completed_tasks_for_date(date: str) -> dict[str, Any]:
    """Get completed tasks for a specific date using efficient API filtering

    Args:
        date: Date in YYYY-MM-DD format (e.g., '2025-06-13')
    """
    api_client = create_api_client()

    try:
        completed_items = api_client.get_done_items(date=date)

        # Group by project for better organization
        by_project: dict[str, list[dict[str, Any]]] = {}
        unassigned: list[dict[str, Any]] = []

        for item in completed_items:
            parent_id = item.get("parentId", "unassigned")

            if parent_id == "unassigned":
                unassigned.append(item)
            else:
                if parent_id not in by_project:
                    by_project[parent_id] = []
                by_project[parent_id].append(item)

        return {
            "date": date,
            "total_completed": len(completed_items),
            "completed_by_project": by_project,
            "unassigned_completed": unassigned,
            "project_count": len(by_project),
            "unassigned_count": len(unassigned),
            "all_completed": completed_items,
            "source": f"Efficiently filtered from /doneItems?date={date}",
        }

    except Exception as e:
        return {
            "date": date,
            "error": str(e),
            "total_completed": 0,
            "completed_by_project": {},
            "unassigned_completed": [],
        }


def start():
    """Start the MCP server"""
    mcp.run()


if __name__ == "__main__":
    start()
