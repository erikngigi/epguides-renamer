"""Main entry point for the Show Management FastAPI application.

This module initializes the FastAPI application instance, mounts the HTTP
routing paths, and wires together the object-oriented API clients. It handles
the application lifecycle hooks (startup/shutdown events) and configures
the Uvicorn production server initialization.

Attributes:
    app (FastAPI): The global FastAPI application instance used for routing
        and middleware configuration.
    show_client (ShowAPIClient): The instantiated singleton client used
        to communicate with the external third-party show service.

Deployment:
    To run this application locally, execute the script directly using `uv`:

        $ uv run python main.py
"""

from typing import Any

from fastapi import FastAPI, Query

from client import ShowAPIClient
from config import settings

app = FastAPI(title="Show Management Service")

# Instantiate the OOP Client
show_client = ShowAPIClient()


@app.get("/all-shows/")
def get_local_shows(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(100, ge=1, le=100, description="Items per page"),
) -> dict[str, Any]:
    """FastAPI endpoint that consume the external OOP API client."""
    data = show_client.fetch_shows(page=page, limit=limit)
    return data


# Clean up client connections when application shuts down
@app.on_event("shutdown")
def shutdown_event() -> None:
    """Executes application cleanup tasks during server shutdown.

    This lifecycle hook is triggered automatically by FastAPI when the Uvicorn
    server begins its teardown process. It ensures that the underlying connection
    pools and socket transports inside `ShowAPIClient` are cleanly closed, preventing
    resource leaks and dangling network connections.
    """
    show_client.close()


if __name__ == "__main__":
    import uvicorn

    # Use the configuration file directly yo boot Uvicorn
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)
