import logging
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


class MarvinAPIClient:
    """API client for Amazing Marvin"""

    def __init__(self, api_key: str):
        """
        Initialize the API client with the API key

        Args:
            api_key: Amazing Marvin API key
        """
        self.api_key = api_key
        self.base_url = "https://serv.amazingmarvin.com/api"  # Removed v1 from URL
        self.headers = {"X-API-Token": api_key}

    def _make_request(
        self, method: str, endpoint: str, data: Optional[Dict] = None
    ) -> Any:
        """Make a request to the API"""
        url = f"{self.base_url}{endpoint}"
        logger.debug(f"Making {method} request to {url}")

        try:
            if method.lower() == "get":
                response = requests.get(url, headers=self.headers)
            elif method.lower() == "post":
                response = requests.post(url, headers=self.headers, json=data)
            elif method.lower() == "put":
                response = requests.put(url, headers=self.headers, json=data)
            elif method.lower() == "delete":
                response = requests.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()

            # Handle 204 No Content responses
            if response.status_code == 204 or not response.content:
                return {}

            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.exception(f"HTTP error: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logger.exception(f"Request error: {e}")
            raise

    def get_tasks(self) -> List[Dict]:
        """Get all tasks and projects (use /todayItems or /dueItems for scheduled/due, or /children for subtasks)"""
        # The Marvin API does not provide a /tasks endpoint. Use /todayItems for scheduled items, /dueItems for due, or /children for subtasks.
        return self._make_request("get", "/todayItems")

    def get_task(self, task_id: str) -> Dict:
        """Get a specific task or project by ID (requires full access token, not supported by default API token)"""
        # The Marvin API does not provide a direct /tasks/{id} endpoint. Use /api/doc?id=... with full access token for arbitrary docs.
        raise NotImplementedError(
            "Direct task lookup by ID is not supported with the standard API token. Use /api/doc?id=... with full access token."
        )

    def get_projects(self) -> List[Dict]:
        """
        Get all projects (as categories with type 'project').

        Note: "Work" and "Personal" are default projects created for most users.
        """
        categories = self.get_categories()
        return [cat for cat in categories if cat.get("type") == "project"]

    def get_categories(self) -> List[Dict]:
        """Get all categories"""
        return self._make_request("get", "/categories")

    def get_labels(self) -> List[Dict]:
        """Get all labels"""
        return self._make_request("get", "/labels")

    def get_due_items(self) -> List[Dict]:
        """Get all due items (experimental endpoint)"""
        return self._make_request("get", "/dueItems")

    def get_children(self, parent_id: str) -> List[Dict]:
        """Get child tasks of a specific parent task or project (experimental endpoint)"""
        try:
            return self._make_request("get", f"/children?parentId={parent_id}")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.warning(
                    f"Children endpoint not available for parent {parent_id}"
                )
                return []
            raise

    def create_task(self, task_data: Dict) -> Dict:
        """Create a new task (uses /addTask endpoint)"""
        return self._make_request("post", "/addTask", data=task_data)

    def mark_task_done(self, item_id: str, timezone_offset: int = 0) -> Dict:
        """Mark a task as done (experimental endpoint)"""
        return self._make_request(
            "post",
            "/markDone",
            data={"itemId": item_id, "timeZoneOffset": timezone_offset},
        )

    def test_api_connection(self) -> str:
        """Test API connection and credentials"""
        url = f"{self.base_url}/test"
        try:
            response = requests.post(url, headers=self.headers)
            response.raise_for_status()
            return response.text.strip()  # Returns "OK" as plain text
        except requests.exceptions.RequestException as e:
            logger.exception(f"API connection test failed: {e}")
            raise

    def start_time_tracking(self, task_id: str) -> Dict:
        """Start time tracking for a task (experimental endpoint)"""
        return self._make_request(
            "post", "/track", data={"taskId": task_id, "action": "START"}
        )

    def stop_time_tracking(self, task_id: str) -> Dict:
        """Stop time tracking for a task (experimental endpoint)"""
        return self._make_request(
            "post", "/track", data={"taskId": task_id, "action": "STOP"}
        )

    def get_time_tracks(self, task_ids: List[str]) -> Dict:
        """Get time tracking data for specific tasks (experimental endpoint)"""
        return self._make_request("post", "/tracks", data={"taskIds": task_ids})

    def claim_reward_points(self, points: int, item_id: str, date: str) -> Dict:
        """Claim reward points for completing a task"""
        return self._make_request(
            "post",
            "/claimRewardPoints",
            data={"points": points, "itemId": item_id, "date": date},
        )

    def get_kudos_info(self) -> Dict:
        """Get kudos information"""
        return self._make_request("get", "/kudos")

    def get_goals(self) -> List[Dict]:
        """Get all goals"""
        return self._make_request("get", "/goals")

    def get_account_info(self) -> Dict:
        """Get account information"""
        return self._make_request("get", "/me")

    def get_currently_tracked_item(self) -> Dict:
        """Get currently tracked item"""
        result = self._make_request("get", "/trackedItem")
        if not result:
            return {"message": "No item currently being tracked"}
        return result

    def create_project(self, project_data: Dict) -> Dict:
        """Create a new project (experimental endpoint)"""
        return self._make_request("post", "/addProject", data=project_data)

    def update_task(self, task_id: str, task_data: Dict) -> Dict:
        """Update a task (requires full access token and /api/doc/update)"""
        raise NotImplementedError(
            "Task update is not supported with the standard API token. Use /api/doc/update with full access token."
        )

    def delete_task(self, task_id: str) -> Dict:
        """Delete a task (requires full access token and /api/doc/delete)"""
        raise NotImplementedError(
            "Task deletion is not supported with the standard API token. Use /api/doc/delete with full access token."
        )
