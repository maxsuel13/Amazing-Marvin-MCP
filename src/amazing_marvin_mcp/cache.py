"""Caching utilities for Amazing Marvin MCP."""

import logging
from datetime import datetime, timedelta

from .api import MarvinAPIClient

logger = logging.getLogger(__name__)

# Constants
CACHE_TTL_MINUTES = 10
CACHE_CLEANUP_HOURS = 1
DATE_FORMAT = "%Y-%m-%d"


class DoneItemsCache:
    """Thread-safe cache for completed items with automatic cleanup."""

    def __init__(self):
        self._cache: dict[str, list[dict]] = {}
        self._expiry: dict[str, datetime] = {}

    def get(self, date: str, api_client: MarvinAPIClient) -> list[dict]:
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

    def get_stats(self) -> dict[str, int]:
        """Get cache statistics."""
        return {
            "cached_dates": len(self._cache),
            "total_cached_items": sum(len(items) for items in self._cache.values()),
        }


# Global cache instance for completed items
done_items_cache = DoneItemsCache()
