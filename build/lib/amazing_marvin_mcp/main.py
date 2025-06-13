import logging
from fastmcp import FastMCP
from typing import Dict, Any

from .api import MarvinAPIClient
from .config import get_settings

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize MCP
mcp = FastMCP(name="amazing-marvin-mcp")


@mcp.tool()
async def get_tasks(query: str = "all") -> Dict[str, Any]:
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
async def get_day(date: str) -> Dict[str, Any]:
    """Get day data from Amazing Marvin for a specific date (YYYY-MM-DD format)"""
    settings = get_settings()
    api_client = MarvinAPIClient(api_key=settings.amazing_marvin_api_key)
    return {"day": api_client.get_day(date), "date": date}


def start():
    """Start the MCP server"""
    mcp.run()

if __name__ == "__main__":
    start()
