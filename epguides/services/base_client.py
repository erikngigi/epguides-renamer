"""Base HTTP client module managing connection lifecycles."""

import httpx


class BaseAPIClient:
    """A foundational API client that manages an isolated HTTPX session pool.

    This class serves as a parent class to provide connection setup and
    teardown capabilities for specialized resource clients.
    """

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")
        # Configure the shared client settings here
        self.client = httpx.Client(follow_redirects=True)

    def close(self) -> None:
        """Safely closes the underlying HTTPX connection pool."""
        self.client.close()
