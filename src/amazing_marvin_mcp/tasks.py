"""Task management functions for Amazing Marvin MCP."""

import logging
from datetime import datetime
from typing import Any

from .api import MarvinAPIClient

logger = logging.getLogger(__name__)


def get_daily_focus(api_client: MarvinAPIClient) -> dict[str, Any]:
    """Get today's focus items - due items, scheduled tasks, and completed tasks."""
    # Get today's items and due items
    today_items = api_client.get_tasks()  # This gets todayItems
    due_items = api_client.get_due_items()

    # Get today's completed tasks (API defaults to today if no date provided)
    today_completed = api_client.get_done_items()

    # Combine scheduled/due items (these are pending by nature from todayItems)
    all_pending_items = []
    item_ids = set()

    for item in today_items + due_items:
        item_id = item.get("_id")
        if item_id and item_id not in item_ids:
            all_pending_items.append(item)
            item_ids.add(item_id)

    # Categorize pending items by priority or type
    high_priority = [
        item for item in all_pending_items if item.get("priority") == "high"
    ]
    projects = [item for item in all_pending_items if item.get("type") == "project"]
    tasks = [item for item in all_pending_items if item.get("type") != "project"]

    return {
        "total_focus_items": len(all_pending_items) + len(today_completed),
        "completed_today": len(today_completed),
        "pending_items": len(all_pending_items),
        "high_priority_items": high_priority,
        "projects": projects,
        "tasks": tasks,
        "completed_items": today_completed,
        "pending_scheduled_items": all_pending_items,
        "productivity_note": f"You've completed {len(today_completed)} items today!"
        if today_completed
        else "No completed items yet today - keep going!",
    }


def batch_create_tasks(
    api_client: MarvinAPIClient,
    task_list: list[Any],
    project_id: str | None = None,
    category_id: str | None = None,
) -> dict[str, Any]:
    """Create multiple tasks at once with optional project/category assignment."""
    created_tasks = []
    failed_tasks = []

    for task_info in task_list:
        try:
            # Handle both string titles and dict objects
            if isinstance(task_info, str):
                task_data = {"title": task_info}
            else:
                task_data = task_info.copy()

            # Add project/category if specified
            if project_id and "parentId" not in task_data:
                task_data["parentId"] = project_id
            if category_id and "categoryId" not in task_data:
                task_data["categoryId"] = category_id

            created_task = api_client.create_task(task_data)
            created_tasks.append(created_task)
        except Exception as e:
            failed_tasks.append({"task": task_info, "error": str(e)})

    return {
        "created_tasks": created_tasks,
        "failed_tasks": failed_tasks,
        "success_count": len(created_tasks),
        "failure_count": len(failed_tasks),
        "total_requested": len(task_list),
    }


def quick_daily_planning(api_client: MarvinAPIClient) -> dict[str, Any]:
    """Get a quick daily planning overview with actionable insights."""
    # Get today's focus items
    today_items = api_client.get_tasks()
    due_items = api_client.get_due_items()

    # Get projects for context
    projects = api_client.get_projects()

    # Analyze workload
    total_due = len(due_items)
    total_scheduled = len(today_items)

    today = datetime.now().strftime("%Y-%m-%d")

    # Simple prioritization suggestions
    heavy_day_threshold = 5
    suggestions = []
    if total_due > 0:
        suggestions.append(f"Focus on {total_due} overdue items first")
    if total_scheduled > heavy_day_threshold:
        suggestions.append("Consider rescheduling some tasks - you have a heavy day")
    if total_scheduled == 0 and total_due == 0:
        suggestions.append("Great! No urgent tasks today - time to work on your goals")

    return {
        "planning_date": today,
        "overdue_items": total_due,
        "scheduled_today": total_scheduled,
        "active_projects": len(projects),
        "suggestions": suggestions,
        "due_items": due_items[:5],  # Show first 5 due items
        "today_items": today_items[:5],  # Show first 5 scheduled items
        "quick_summary": f"{total_due} due, {total_scheduled} scheduled",
    }
