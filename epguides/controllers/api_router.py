"""API controller handling television show data routing.

This module encapsulates all JSON-based REST endpoints for the television show
domain, acting as the Controller layer in the MVC architecture.
"""

from typing import Any, Dict

from fastapi import APIRouter, Query

from epguides.services.client import ShowAPIClient

router = APIRouter()

show_client = ShowAPIClient()


@router.get("/all-shows/")
def get_all_shows(
    page: int = Query(1, ge=1, description="Page Number"),
    limit: int = Query(100, ge=1, le=100, description="Items per page"),
) -> Dict[str, Any]:
    """FastAPI endpoint that consumes the external OOP API client.

    This route acts as the controller handler, fetching structured show
    metadata from the underlying service layer and exposing it to the web.
    """
    data = show_client.fetch_shows(page=page, limit=limit)
    return data


@router.get("/search-show/")
def search_show(
    query: str = Query("wire", description="Search for any Tv Show"),
) -> list[Any]:
    data = show_client.search_shows(query=query)
    return data
