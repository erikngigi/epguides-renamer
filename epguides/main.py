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

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from epguides.controllers.api_router import router as api_router
from epguides.services.client import ShowAPIClient
from epguides.settings import settings

app = FastAPI(docs_url=None, title="Epguides Middleware API")

app.mount("/static", StaticFiles(directory="epguides/static"), name="static")

# Instantiate the OOP Client
show_client = ShowAPIClient()

app.include_router(api_router, prefix="/api/v1", tags=["Shows"])


@app.get("/docs", include_in_schema=False)
def custom_swagger_ui_html() -> HTMLResponse:
    """Renders a highly customized, standalone instance of the Swagger UI documentation."""
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Epguides Middleware API",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        swagger_favicon_url="/static/tv-icon.png",
    )


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
    uvicorn.run("epguides.main:app", host=settings.host, port=settings.port, reload=True)
