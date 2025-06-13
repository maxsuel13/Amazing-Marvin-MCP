"""Utility functions for Amazing Marvin MCP that can be tested independently."""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from .api import MarvinAPIClient
from .config import get_settings

logger = logging.getLogger(__name__)


def create_project_with_tasks_util(
    project_title: str, task_titles: List[str], project_type: str = "project"
) -> Dict[str, Any]:
    """Create a project with multiple tasks at once"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)

    # Create the project
    project_data = {"title": project_title, "type": project_type}
    created_project = api_client.create_project(project_data)
    project_id = created_project.get("_id")

    # Create tasks in the project
    created_tasks = []
    if project_id:
        for task_title in task_titles:
            task_data = {"title": task_title, "parentId": project_id}
            created_task = api_client.create_task(task_data)
            created_tasks.append(created_task)

    return {
        "created_project": created_project,
        "created_tasks": created_tasks,
        "task_count": len(created_tasks),
    }


def get_project_overview_util(project_id: str) -> Dict[str, Any]:
    """Get comprehensive overview of a project including tasks and progress"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)

    # Get project children
    children = api_client.get_children(project_id)

    # Analyze the tasks
    total_tasks = len(children)
    completed_tasks = sum(1 for task in children if task.get("done", False))
    pending_tasks = total_tasks - completed_tasks
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    # Get project info (from categories since projects are categories)
    categories = api_client.get_categories()
    project_info = next(
        (cat for cat in categories if cat.get("_id") == project_id), None
    )

    return {
        "project_id": project_id,
        "project_info": project_info,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "completion_rate": round(completion_rate, 2),
        "tasks": children,
    }


def get_daily_focus_util() -> Dict[str, Any]:
    """Get today's focus items - due items and scheduled tasks"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)

    # Get today's items and due items
    today_items = api_client.get_tasks()  # This gets todayItems
    due_items = api_client.get_due_items()

    # Combine and deduplicate
    all_focus_items = []
    item_ids = set()

    for item in today_items + due_items:
        item_id = item.get("_id")
        if item_id and item_id not in item_ids:
            all_focus_items.append(item)
            item_ids.add(item_id)

    # Categorize by priority or type
    high_priority = [item for item in all_focus_items if item.get("priority") == "high"]
    projects = [item for item in all_focus_items if item.get("type") == "project"]
    tasks = [item for item in all_focus_items if item.get("type") != "project"]

    return {
        "total_focus_items": len(all_focus_items),
        "high_priority_items": high_priority,
        "projects": projects,
        "tasks": tasks,
        "all_items": all_focus_items,
    }


def get_productivity_summary_util() -> Dict[str, Any]:
    """Get productivity summary with goals progress and tracking status"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)

    today = datetime.now().strftime("%Y-%m-%d")

    # Get goals
    goals = api_client.get_goals()

    # Get account info for streaks/stats
    account = api_client.get_account_info()

    # Get currently tracked item
    tracked_item = api_client.get_currently_tracked_item()

    return {
        "date": today,
        "active_goals": len(goals),
        "goals": goals,
        "account_stats": account,
        "currently_tracking": tracked_item,
        "summary": f"You have {len(goals)} active goals",
    }


def batch_create_tasks_util(
    task_list: List[Any],
    project_id: Optional[str] = None,
    category_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Create multiple tasks at once with optional project/category assignment"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)

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


def quick_daily_planning_util() -> Dict[str, Any]:
    """Get a quick daily planning overview with actionable insights"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)

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


def get_completed_tasks_util() -> Dict[str, Any]:
    """Get completed tasks by filtering from available sources

    Note: Due to API limitations, this may not include all historical completed tasks.
    It checks today's items, project children, and unassigned tasks for completed ones.
    """
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)

    completed_tasks = []
    sources_checked = []

    # Check today's items for completed ones
    try:
        today_items = api_client.get_tasks()
        completed_today = [task for task in today_items if task.get("done", False)]
        completed_tasks.extend(completed_today)
        sources_checked.append("today_items")
    except Exception:
        logger.warning("Could not check today's items")

    # Check projects for completed tasks
    try:
        projects = api_client.get_projects()
        for project in projects:
            project_id = project.get("_id")
            if project_id:
                children = api_client.get_children(project_id)
                completed_children = [
                    task for task in children if task.get("done", False)
                ]
                completed_tasks.extend(completed_children)
        sources_checked.append("project_children")
    except Exception:
        logger.warning("Could not check project children")

    # Check for unassigned completed tasks
    try:
        unassigned = api_client.get_children("unassigned")
        completed_unassigned = [task for task in unassigned if task.get("done", False)]
        completed_tasks.extend(completed_unassigned)
        sources_checked.append("unassigned_tasks")
    except Exception:
        logger.warning("Could not check unassigned tasks")

    # Remove duplicates based on task ID
    unique_completed = []
    seen_ids = set()
    for task in completed_tasks:
        task_id = task.get("_id")
        if task_id and task_id not in seen_ids:
            unique_completed.append(task)
            seen_ids.add(task_id)

    return {
        "completed_tasks": unique_completed,
        "total_completed": len(unique_completed),
        "sources_checked": sources_checked,
        "limitations": "This search is limited to tasks visible through available API endpoints and may not include all historical completed tasks",
        "recommendation": "For comprehensive completed task history, consider using the Amazing Marvin app directly",
    }
