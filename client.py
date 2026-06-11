"""API client module for consuming external show data.

This module provides an object-oriented interface to interact with third-party
television show APIs. It encapsulates connection management, query parameter
serialization, and network error handling using HTTPX.

Example:
    >>> client = ShowAPIClient()
    >>> data = client.fetch_shows(page=1, limit=10)
    >>> print(data)
    >>> client.close()
"""

from typing import Any, Dict

import httpx

from config import settings


class ShowAPIClient:
    """An HTTP client wrapper for interacting with the external Shows API.

    This class abstracts network requests to the configured endpoints, managing
    the persistent client session and formatting outbound parameters.

    Attributes:
        base_url (str): The sanitized base URL of the target API service.
        endpoint (str): The sanitized endpoint path for show resources.
        target_url (str): The absolute computed URL endpoint for requests.
        client (httpx.Client): The underlying synchronous HTTP client used
            for connection pooling.
    """

    def __init__(self) -> None:
        """Intializes the API client with target URLs and session instances."""
        self.base_url = settings.base_api_url.rstrip("/")
        self.endpoint = settings.all_shows_endpoint.lstrip("/")
        self.target_url = f"{self.base_url}/{self.endpoint}"
        self.client = httpx.Client()

    def fetch_shows(self, page: int = 1, limit: int = 100) -> Dict[str, Any]:
        """Fetches a paginated list of television shows from the remote server.

        Args:
            page (int, optional): The page number to retrieve. Defaults to 1.
            limit (int, optional): The maximum number of records to return per
                page. Defaults to 10.

        Returns:
            Dict[str, Any]: The parsed JSON response containing show entities
                on success, or an error payload on failure.
        """
        params = {"page": page, "limit": limit}

        try:
            response = self.client.get(self.target_url, params=params)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict):
                return data

            return {"error:": "API did not return a JSON object/dictionary"}
        except httpx.HTTPStatusError as exc:
            return {"error": f"External API error: {exc.response.status_code}"}
        except httpx.RequestError as exc:
            return {"error": f"An error occurred while requesting: {exc}"}

    def close(self) -> None:
        """Closes the underlying HTTPX client transport and connection pool.

        This method should be called during application shutdown to prevent
        leaking unclosed sockets.
        """
        self.client.close()
