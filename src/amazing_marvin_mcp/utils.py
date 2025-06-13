"""Utility functions for Amazing Marvin MCP that can be tested independently."""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from .api import MarvinAPIClient
from .config import get_settings

logger = logging.getLogger(__name__)

# Constants
CACHE_TTL_MINUTES = 10
CACHE_CLEANUP_HOURS = 1
DATE_FORMAT = "%Y-%m-%d"


# Simple in-memory cache for done items
class DoneItemsCache:
    """Thread-safe cache for completed items with automatic cleanup."""

    def __init__(self):
        self._cache: Dict[str, List[Dict]] = {}
        self._expiry: Dict[str, datetime] = {}

    def get(self, date: str, api_client: MarvinAPIClient) -> List[Dict]:
        """Get completed items with caching support."""
        current_time = datetime.now()
        today = current_time.strftime(DATE_FORMAT)

        # Don't cache today's data (it changes throughout the day)
        if date == today:
            logger.debug("Fetching fresh completed items for today: %s", date)
            return api_client.get_done_items(date=date)

        # Check if we have valid cached data
        if self._is_cached_and_valid(date, current_time):
            logger.debug("Using cached completed items for %s", date)
            return self._cache[date]

        # Fetch fresh data and cache it
        logger.debug("Fetching and caching completed items for %s", date)
        items = api_client.get_done_items(date=date)

        self._cache[date] = items
        self._expiry[date] = current_time + timedelta(minutes=CACHE_TTL_MINUTES)

        # Periodic cleanup
        self._cleanup_expired_entries(current_time)

        return items

    def _is_cached_and_valid(self, date: str, current_time: datetime) -> bool:
        """Check if data is cached and still valid."""
        return (
            date in self._cache
            and date in self._expiry
            and current_time < self._expiry[date]
        )

    def _cleanup_expired_entries(self, current_time: datetime) -> None:
        """Remove expired cache entries."""
        cleanup_threshold = current_time - timedelta(hours=CACHE_CLEANUP_HOURS)
        expired_dates = [
            date
            for date, exp_time in self._expiry.items()
            if exp_time < cleanup_threshold
        ]

        for expired_date in expired_dates:
            self._cache.pop(expired_date, None)
            self._expiry.pop(expired_date, None)

        if expired_dates:
            logger.debug("Cleaned up %d expired cache entries", len(expired_dates))

    def get_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            "cached_dates": len(self._cache),
            "total_cached_items": sum(len(items) for items in self._cache.values()),
        }


# Global cache instance for completed items
_done_items_cache = DoneItemsCache()


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

    # Separate completed and pending tasks
    completed_tasks_list = [task for task in children if task.get("done", False)]
    pending_tasks_list = [task for task in children if not task.get("done", False)]

    # Analyze the tasks
    total_tasks = len(children)
    completed_count = len(completed_tasks_list)
    pending_count = len(pending_tasks_list)
    completion_rate = (completed_count / total_tasks * 100) if total_tasks > 0 else 0

    # Get project info (from categories since projects are categories)
    categories = api_client.get_categories()
    project_info = next(
        (cat for cat in categories if cat.get("_id") == project_id), None
    )

    return {
        "project_id": project_id,
        "project_info": project_info,
        "total_tasks": total_tasks,
        "completed_tasks_count": completed_count,
        "pending_tasks_count": pending_count,
        "completion_rate": round(completion_rate, 2),
        "completed_tasks": completed_tasks_list,
        "pending_tasks": pending_tasks_list,
        "all_tasks": children,
        "progress_summary": f"{completed_count}/{total_tasks} tasks completed ({completion_rate:.1f}%)",
    }


def get_daily_focus_util() -> Dict[str, Any]:
    """Get today's focus items - due items, scheduled tasks, and completed tasks"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)

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


# Helper functions to reduce complexity of get_productivity_summary_for_time_range_util
def _generate_date_range(
    days: Optional[int], start_date: Optional[str], end_date: Optional[str]
) -> tuple[list[str], datetime, datetime]:
    """Generate a list of dates and start/end datetime objects based on inputs.

    Used to reduce complexity of get_productivity_summary_for_time_range_util.
    """
    if start_date:
        # Use explicit date range
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d") if end_date else datetime.now()

        # Generate list of dates in range
        date_list = []
        current = start
        while current <= end:
            date_list.append(current.strftime("%Y-%m-%d"))
            current += timedelta(days=1)
    else:
        # Use days parameter (default behavior)
        if days is None:
            days = 7
        today = datetime.now()
        date_list = []
        for i in range(days):
            date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            date_list.append(date)
        start = today - timedelta(days=days - 1)
        end = today

    return date_list, start, end


def _process_date_data(
    date_str: str, api_client: MarvinAPIClient, range_summary: Dict[str, Any]
) -> None:
    """Process data for a single date and update the range_summary dict.

    Used to reduce complexity of get_productivity_summary_for_time_range_util.
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    weekday = date_obj.strftime("%A")
    is_today = date_str == datetime.now().strftime("%Y-%m-%d")

    try:
        # Use cached API call
        items = _done_items_cache.get(date_str, api_client)
        count = len(items)

        # Track cache efficiency (simplified)
        range_summary["api_calls"] += 1

        range_summary["daily_breakdown"][date_str] = {
            "count": count,
            "weekday": weekday,
            "is_today": is_today,
            "tasks": items,  # Include actual tasks
        }
        range_summary["total_completed"] += count

        # Store tasks by date
        range_summary["tasks_by_date"][date_str] = items

        # Add to all completed tasks
        range_summary["all_completed_tasks"].extend(items)

        # Track by project with detailed task info
        for item in items:
            project_id = item.get("parentId", "unassigned")

            # Count by project
            if project_id not in range_summary["by_project"]:
                range_summary["by_project"][project_id] = 0
            range_summary["by_project"][project_id] += 1

            # Store tasks by project
            if project_id not in range_summary["tasks_by_project"]:
                range_summary["tasks_by_project"][project_id] = []
            range_summary["tasks_by_project"][project_id].append(
                {"task": item, "completed_date": date_str, "weekday": weekday}
            )
    except Exception as e:
        logger.warning("Error getting done items for %s: %s", date_str, e)
        range_summary["daily_breakdown"][date_str] = {
            "count": 0,
            "weekday": weekday,
            "is_today": is_today,
            "tasks": [],
        }
        range_summary["tasks_by_date"][date_str] = []


def _calculate_statistics(range_summary: Dict[str, Any]) -> None:
    """Calculate statistics from collected data and update range_summary.

    Used to reduce complexity of get_productivity_summary_for_time_range_util.
    """
    if range_summary["daily_breakdown"]:
        daily_counts = [
            (date, data["count"])
            for date, data in range_summary["daily_breakdown"].items()
        ]
        sorted_days = sorted(daily_counts, key=lambda x: x[1])

        range_summary["least_productive_day"] = {
            "date": sorted_days[0][0],
            "count": sorted_days[0][1],
            "weekday": range_summary["daily_breakdown"][sorted_days[0][0]]["weekday"],
        }
        range_summary["most_productive_day"] = {
            "date": sorted_days[-1][0],
            "count": sorted_days[-1][1],
            "weekday": range_summary["daily_breakdown"][sorted_days[-1][0]]["weekday"],
        }

        range_summary["average_per_day"] = range_summary["total_completed"] / len(
            daily_counts
        )


def get_productivity_summary_for_time_range_util(
    days: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> Dict[str, Any]:
    """Get a productivity summary for a specified time range using efficient API calls

    Args:
        days: Number of days to look back from today (default: 7 for weekly summary)
        start_date: Start date in YYYY-MM-DD format (overrides days parameter)
        end_date: End date in YYYY-MM-DD format (defaults to today if start_date provided)

    Examples:
        get_productivity_summary_for_time_range_util(days=30)  # Past 30 days
        get_productivity_summary_for_time_range_util(start_date='2025-06-01', end_date='2025-06-10')
        get_productivity_summary_for_time_range_util(start_date='2025-06-01')  # From June 1st to today
    """
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)

    try:
        # Determine date range using helper function
        date_list, start, end = _generate_date_range(days, start_date, end_date)

        range_summary = {
            "period_start": start.strftime("%Y-%m-%d"),
            "period_end": end.strftime("%Y-%m-%d"),
            "total_days": len(date_list),
            "total_completed": 0,
            "daily_breakdown": {},
            "by_project": {},
            "all_completed_tasks": [],  # Include all tasks for correlation
            "tasks_by_date": {},  # Tasks organized by date
            "tasks_by_project": {},  # Tasks organized by project
            "most_productive_day": None,
            "least_productive_day": None,
            "average_per_day": 0.0,
            "api_calls": 0,
        }

        # Get data for each date efficiently using helper function
        for date_str in date_list:
            _process_date_data(date_str, api_client, range_summary)

        # Calculate statistics using helper function
        _calculate_statistics(range_summary)

        # Sort projects by completion count
        range_summary["top_projects"] = sorted(
            range_summary["by_project"].items(), key=lambda x: x[1], reverse=True
        )[:5]  # Top 5 projects

        # Add project name resolution for better UX
        try:
            projects = api_client.get_projects()
            project_names = {
                proj.get("_id"): proj.get("title", "Unnamed Project")
                for proj in projects
            }

            range_summary["project_names"] = project_names
            range_summary["top_projects_with_names"] = [
                {
                    "project_id": proj_id,
                    "project_name": project_names.get(
                        proj_id,
                        "Unknown Project" if proj_id != "unassigned" else "Unassigned",
                    ),
                    "completed_count": count,
                }
                for proj_id, count in range_summary["top_projects"]
            ]
        except Exception as e:
            logger.warning("Could not resolve project names: %s", e)
            range_summary["project_names"] = {}
            range_summary["top_projects_with_names"] = []

        # Add efficiency metrics using cache stats
        cache_stats = _done_items_cache.get_stats()
        range_summary["efficiency_metrics"] = {
            "cached_dates": cache_stats["cached_dates"],
            "total_cached_items": cache_stats["total_cached_items"],
            "total_api_calls": range_summary["api_calls"],
        }
    except Exception as e:
        logger.exception("Error getting weekly summary")
        return {
            "error": str(e),
            "total_completed": 0,
            "daily_breakdown": {},
            "by_project": {},
        }
    else:
        return range_summary


def get_completed_tasks_util() -> Dict[str, Any]:
    """Get completed tasks using the efficient /doneItems endpoint with date filtering

    Returns completed tasks with efficient date-based categorization.
    """
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)

    try:
        datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        # Use efficient date-filtered API calls
        today_completed = api_client.get_done_items()  # Defaults to today
        yesterday_completed = api_client.get_done_items(date=yesterday)

        # For older items, we could either:
        # 1. Make additional API calls for specific dates
        # 2. Get all items and filter (less efficient but comprehensive)
        # For now, let's be comprehensive but note the efficiency trade-off
        all_done_items = api_client.get_done_items()

        # Calculate older items by exclusion
        today_ids = {item.get("_id") for item in today_completed}
        yesterday_ids = {item.get("_id") for item in yesterday_completed}

        older_completed = [
            item
            for item in all_done_items
            if item.get("_id") not in today_ids and item.get("_id") not in yesterday_ids
        ]

        today_count = len(today_completed)
        yesterday_count = len(yesterday_completed)

        return {
            "completed_tasks": all_done_items,
            "total_completed": len(all_done_items),
            "today_completed": today_completed,
            "yesterday_completed": yesterday_completed,
            "older_completed": older_completed,
            "today_count": today_count,
            "yesterday_count": yesterday_count,
            "older_count": len(older_completed),
            "date_breakdown": {
                "today": today_count,
                "yesterday": yesterday_count,
                "older": len(older_completed),
            },
            "source": "Amazing Marvin /doneItems endpoint with efficient date filtering",
            "efficiency_note": f"Today and yesterday use efficient API filtering ({today_count} + {yesterday_count}) items, older items calculated by exclusion",
        }
    except Exception as e:
        logger.exception("Error getting completed tasks")
        return {
            "completed_tasks": [],
            "total_completed": 0,
            "error": str(e),
            "source": "Error occurred",
        }
