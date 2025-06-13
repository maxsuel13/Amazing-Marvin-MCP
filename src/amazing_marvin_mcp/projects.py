"""Project management functions for Amazing Marvin MCP."""

import logging
from typing import Any, Dict, List

from .api import MarvinAPIClient

logger = logging.getLogger(__name__)


def create_project_with_tasks(
    api_client: MarvinAPIClient,
    project_title: str,
    task_titles: List[str],
    project_type: str = "project",
) -> Dict[str, Any]:
    """Create a project with multiple tasks at once."""
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


def get_project_overview(
    api_client: MarvinAPIClient, project_id: str
) -> Dict[str, Any]:
    """Get comprehensive overview of a project including tasks and progress."""
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
