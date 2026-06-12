"""Specialized resource clients for interacting with distinct API domains."""

from typing import Any, Dict, Optional, cast

import httpx

from epguides.config.settings import settings
from epguides.services.base_client import BaseAPIClient


class ShowAPIClient(BaseAPIClient):
    """Client for managing operations related to the /shows endpoint."""

    def __init__(self) -> None:
        # Call the parent class __init__ and pass the global base URL
        super().__init__(base_url=settings.base_api_url)
        # Define this client's unique path
        self.target_url = f"{self.base_url}/{settings.all_shows_endpoint.lstrip('/')}"

    def fetch_shows(self, page: int = 1, limit: int = 100) -> Dict[str, Any]:
        """Fetches a paginated list of shows."""
        params = {"page": page, "limit": limit}
        try:
            response = self.client.get(self.target_url, params=params)
            response.raise_for_status()
            return cast(Dict[str, Any], response.json())
        except httpx.HTTPError as exc:
            return {"error": f"Network error: {exc}"}

    def search_shows(self, query: str) -> list[Any] | dict[str, Any]:
        """Searches for a specific TV show by its name string fragment.

        Args:
            query (str): The search phrase or title piece of the target show.

        Returns:
            list[Any]: A list of matched show dictionaries if successful,
                or an error dictionary containing diagnostic details on failure.
        """
        search_url = f"{self.target_url.rstrip('/')}/{settings.search_shows_endpoint}"

        params: dict[str, Any] = {"query": query}

        try:
            response = self.client.get(search_url, params=params)
            response.raise_for_status()
            return cast(list[Any], response.json())
        except httpx.HTTPError as exc:
            return {"error": f"Search endpoint failed: {exc}"}

    def fetch_show_metadata(self, epguides_key: str) -> dict[str, Any]:
        """Fetches the metadata of a specific TV show using the TV Shows epguides_key.

        Args:
            epguides_key (str): The key of the target show.

        Returns:
            dict[str, Any]: A dictionary of the matched show metadata if successful.
        """
        search_url = f"{self.target_url.rstrip('/')}/{epguides_key}"

        try:
            response = self.client.get(search_url)
            response.raise_for_status()
            return cast(dict[str, Any], response.json())
        except httpx.HTTPError as exc:
            return {"error": f"Search endpoint failed: {exc}"}
