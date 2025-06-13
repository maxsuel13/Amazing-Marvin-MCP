import requests
from typing import Dict, List, Any, Optional
import logging

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
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Any:
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
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            raise
    
    def get_tasks(self) -> List[Dict]:
        """Get all tasks and projects (use /todayItems or /dueItems for scheduled/due, or /children for subtasks)"""
        # The Marvin API does not provide a /tasks endpoint. Use /todayItems for scheduled items, /dueItems for due, or /children for subtasks.
        return self._make_request("get", "/todayItems")
    
    def get_task(self, task_id: str) -> Dict:
        """Get a specific task or project by ID (requires full access token, not supported by default API token)"""
        # The Marvin API does not provide a direct /tasks/{id} endpoint. Use /api/doc?id=... with full access token for arbitrary docs.
        raise NotImplementedError("Direct task lookup by ID is not supported with the standard API token. Use /api/doc?id=... with full access token.")
    
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
    
    def get_strategies(self) -> List[Dict]:
        """Get all strategies"""
        return self._make_request("get", "/strategies")
    
    def get_day(self, date: str) -> Dict:
        """Get day by date (YYYY-MM-DD format)"""
        return self._make_request("get", f"/day/{date}")
    
    def create_task(self, task_data: Dict) -> Dict:
        """Create a new task (uses /addTask endpoint)"""
        return self._make_request("post", "/addTask", data=task_data)
    
    def update_task(self, task_id: str, task_data: Dict) -> Dict:
        """Update a task (requires full access token and /api/doc/update)"""
        raise NotImplementedError("Task update is not supported with the standard API token. Use /api/doc/update with full access token.")
    
    def delete_task(self, task_id: str) -> Dict:
        """Delete a task (requires full access token and /api/doc/delete)"""
        raise NotImplementedError("Task deletion is not supported with the standard API token. Use /api/doc/delete with full access token.")
