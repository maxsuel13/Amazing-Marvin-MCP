"""Pytest tests for Amazing Marvin MCP API functionality."""

from datetime import datetime

import pytest
import requests
from amazing_marvin_mcp.api import MarvinAPIClient
from amazing_marvin_mcp.config import get_settings


@pytest.fixture()
def api_client():
    """Create API client for testing."""
    try:
        settings = get_settings()
        if not settings.amazing_marvin_api_key:
            pytest.skip("No API key available for testing")
        return MarvinAPIClient(api_key=settings.amazing_marvin_api_key)
    except Exception:
        pytest.skip("Configuration error - cannot create API client")


@pytest.fixture()
def created_items():
    """Track created items for cleanup attempts."""
    items = {"projects": [], "tasks": []}
    yield items
    # Note: Cleanup not possible with standard API token
    # Items will remain in Amazing Marvin account
    if items["projects"] or items["tasks"]:
        pass


@pytest.fixture()
def test_project_data():
    """Test project data."""
    return {
        "title": f"[TEST] Pytest Project - {datetime.now().strftime('%H:%M:%S')}",
        "type": "project",
    }


@pytest.fixture()
def test_task_data():
    """Test task data."""
    return {
        "title": f"[TEST] Pytest Task - {datetime.now().strftime('%H:%M:%S')}",
        "note": "This is a test task created by pytest - safe to delete",
    }


class TestMarvinAPIClient:
    """Test the MarvinAPIClient class."""

    def test_api_connection(self, api_client):
        """Test API connection."""
        result = api_client.test_api_connection()
        assert result == "OK"

    def test_get_categories(self, api_client):
        """Test getting categories."""
        categories = api_client.get_categories()
        assert isinstance(categories, list)

    def test_get_projects(self, api_client):
        """Test getting projects."""
        projects = api_client.get_projects()
        assert isinstance(projects, list)

    def test_get_labels(self, api_client):
        """Test getting labels."""
        labels = api_client.get_labels()
        assert isinstance(labels, list)

    def test_get_due_items(self, api_client):
        """Test getting due items."""
        due_items = api_client.get_due_items()
        assert isinstance(due_items, list)

    def test_get_goals(self, api_client):
        """Test getting goals."""
        goals = api_client.get_goals()
        assert isinstance(goals, list)

    def test_get_account_info(self, api_client):
        """Test getting account info."""
        account = api_client.get_account_info()
        assert isinstance(account, dict)

    def test_get_currently_tracked_item(self, api_client):
        """Test getting currently tracked item."""
        tracked = api_client.get_currently_tracked_item()
        assert tracked is not None


class TestTaskAndProjectManagement:
    """Test task and project creation, modification, and deletion."""

    def test_create_project(self, api_client, test_project_data, created_items):
        """Test creating a project."""
        created_project = api_client.create_project(test_project_data)
        created_items["projects"].append(created_project.get("_id"))
        assert created_project is not None
        assert created_project.get("title") == test_project_data["title"]
        assert "_id" in created_project

    def test_create_task(self, api_client, test_task_data, created_items):
        """Test creating a task."""
        created_task = api_client.create_task(test_task_data)
        created_items["tasks"].append(created_task.get("_id"))
        assert created_task is not None
        assert created_task.get("title") == test_task_data["title"]
        assert "_id" in created_task

    def test_comprehensive_workflow(
        self, api_client, test_project_data, test_task_data, created_items
    ):
        """Test a complete workflow: create project, add tasks, manage tasks."""
        # Create test project
        created_project = api_client.create_project(test_project_data)
        project_id = created_project.get("_id")
        created_items["projects"].append(project_id)
        assert project_id is not None

        # Create tasks in the project
        test_tasks = []
        for i in range(3):
            task_data = {
                **test_task_data,
                "title": f"{test_task_data['title']} #{i + 1}",
                "parentId": project_id,
            }
            created_task = api_client.create_task(task_data)
            created_items["tasks"].append(created_task.get("_id"))
            test_tasks.append(created_task)
            assert created_task.get("_id") is not None

        # Test getting children of the project
        children = api_client.get_children(project_id)
        assert isinstance(children, list)
        # Note: children might be empty if the endpoint is experimental

        # Mark first task as done
        if test_tasks and test_tasks[0].get("_id"):
            task_id = test_tasks[0]["_id"]
            completed = api_client.mark_task_done(task_id)
            assert completed is not None


class TestTimeTracking:
    """Test time tracking functionality."""

    def test_start_stop_tracking(self, api_client, test_task_data, created_items):
        """Test starting and stopping time tracking."""
        # First create a task to track
        created_task = api_client.create_task(test_task_data)
        task_id = created_task.get("_id")
        created_items["tasks"].append(task_id)
        assert task_id is not None

        # Test starting tracking
        start_result = api_client.start_time_tracking(task_id)
        assert start_result is not None

        # Test stopping tracking
        stop_result = api_client.stop_time_tracking(task_id)
        assert stop_result is not None

    def test_get_time_tracks(self, api_client, test_task_data, created_items):
        """Test getting time tracking data."""
        # Create a task first
        created_task = api_client.create_task(test_task_data)
        task_id = created_task.get("_id")
        created_items["tasks"].append(task_id)
        assert task_id is not None

        # Get time tracks for the task
        tracks = api_client.get_time_tracks([task_id])
        assert tracks is not None


class TestRewards:
    """Test reward system functionality."""

    def test_claim_reward_points(self, api_client, test_task_data, created_items):
        """Test claiming reward points."""
        # Create and complete a task first
        created_task = api_client.create_task(test_task_data)
        task_id = created_task.get("_id")
        created_items["tasks"].append(task_id)
        assert task_id is not None

        # Mark task as done
        completed_task = api_client.mark_task_done(task_id)
        assert completed_task is not None

        # Try to claim reward points (might fail due to API restrictions)
        today = datetime.now().strftime("%Y-%m-%d")
        try:
            reward_result = api_client.claim_reward_points(10, task_id, today)
            assert reward_result is not None
        except Exception as e:
            # Reward claiming might not be available for all accounts
            pytest.skip(f"Reward claiming not available: {e}")

    def test_get_kudos_info(self, api_client):
        """Test getting kudos information."""
        kudos = api_client.get_kudos_info()
        assert kudos is not None


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_invalid_api_key(self):
        """Test behavior with invalid API key."""
        invalid_client = MarvinAPIClient(api_key="invalid_key")
        with pytest.raises(requests.exceptions.RequestException):
            invalid_client.get_categories()

    def test_invalid_task_id(self, api_client):
        """Test behavior with invalid task ID."""
        with pytest.raises(requests.exceptions.RequestException):
            api_client.mark_task_done("invalid_task_id")

    def test_invalid_project_id(self, api_client):
        """Test behavior with invalid project ID."""
        children = api_client.get_children("invalid_project_id")
        # Should return empty list due to error handling
        assert isinstance(children, list)


class TestProjectPlanningEnhancements:
    """Test the new project planning enhancement features."""

    def test_create_project_with_tasks(self, test_project_data, created_items):
        """Test creating a project with multiple tasks at once."""
        from amazing_marvin_mcp.utils import create_project_with_tasks_util

        task_titles = ["Task 1", "Task 2", "Task 3"]
        result = create_project_with_tasks_util(
            project_title=test_project_data["title"],
            task_titles=task_titles,
            project_type=test_project_data["type"],
        )

        # Track created items
        created_items["projects"].append(result["created_project"].get("_id"))
        for task in result["created_tasks"]:
            created_items["tasks"].append(task.get("_id"))

        assert result["created_project"] is not None
        expected_task_count = 3
        assert result["task_count"] == expected_task_count
        assert len(result["created_tasks"]) == expected_task_count

    def test_get_daily_focus(self):
        """Test getting daily focus items."""
        from amazing_marvin_mcp.utils import get_daily_focus_util

        result = get_daily_focus_util()

        assert "total_focus_items" in result
        assert "high_priority_items" in result
        assert "projects" in result
        assert "tasks" in result

    def test_get_productivity_summary(self):
        """Test getting productivity summary."""
        from amazing_marvin_mcp.utils import get_productivity_summary_util

        result = get_productivity_summary_util()

        assert "date" in result
        assert "active_goals" in result
        assert "summary" in result

    def test_quick_daily_planning(self):
        """Test quick daily planning feature."""
        from amazing_marvin_mcp.utils import quick_daily_planning_util

        result = quick_daily_planning_util()

        assert "planning_date" in result
        assert "suggestions" in result
        assert "quick_summary" in result
        assert isinstance(result["suggestions"], list)

    def test_batch_create_tasks(self, created_items):
        """Test batch task creation."""
        from amazing_marvin_mcp.utils import batch_create_tasks_util

        task_count = 3
        task_list = ["Batch Task 1", "Batch Task 2", "Batch Task 3"]
        result = batch_create_tasks_util(task_list=task_list)

        # Track created tasks
        for task in result["created_tasks"]:
            created_items["tasks"].append(task.get("_id"))

        assert "created_tasks" in result
        assert "success_count" in result
        assert result["success_count"] >= 0
        assert result["total_requested"] == task_count

    def test_get_completed_tasks(self):
        """Test getting completed tasks."""
        from amazing_marvin_mcp.utils import get_completed_tasks_util

        result = get_completed_tasks_util()

        assert "completed_tasks" in result
        assert "total_completed" in result
        assert "sources_checked" in result
        assert "limitations" in result
        assert isinstance(result["completed_tasks"], list)
        assert isinstance(result["sources_checked"], list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
