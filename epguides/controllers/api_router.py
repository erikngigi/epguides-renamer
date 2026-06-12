"""API controller handling television show data routing.

This module encapsulates all JSON-based REST endpoints for the television show
domain, acting as the Controller layer in the MVC architecture.
"""

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query

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
    query: str = Query(..., description="The name of the TV show to search for"),
    network: Optional[str] = Query(None, description="Optional TV Network filter (e.g., 'HBO', 'CW', 'Paramount')"),
) -> list[Any] | Dict[str, Any]:
    """Endpoint that delegates searches down to the OOP client server layer.

    If a network parameter is provided, the raw list is filtered locally.
    """

    search_show_data = show_client.search_shows(query=query)

    # Guard: If it's an error dictionary payload, return it immediately
    if isinstance(search_show_data, dict) and "error" in search_show_data:
        return search_show_data

    # Local Filter: If the user provided a network, filter the list in python
    if network is not None and isinstance(search_show_data, list):
        search_show_data = [show for show in search_show_data if show.get("network", "").lower() == network.lower()]

    # Deep Fetch: Turn keys into full metadata objects
    if isinstance(search_show_data, list):
        # Extract the keys just like before
        # Guard: If no shows matched your filters, return an empty dictionary
        # if not search_show_data:
        #     raise HTTPException(status_code=404, detail="No matching show found with those parameters")

        # Grab the very FIRST show that matched
        # first_match = search_show_data[0]
        # target_key = first_match.get("epguides_key")

        # if target_key:
        #     # Fetch and return the deep metadata directly
        #     show_metadata = show_client.fetch_show_metadata(epguides_key=target_key)
        # return show_metadata

        # Extract the keys just like you did before
        extracted_keys: list[str] = [show["epguides_key"] for show in search_show_data if "epguides_key" in show]
        # multiple_shows_metadata = {key: show_client.fetch_show_metadata(epguides_key=key) for key in extracted_keys}

        # Use a list comprehension to hit your new fetch_show_metadata method for each key
        multiple_shows_metadata = [show_client.fetch_show_metadata(epguides_key=key) for key in extracted_keys]

        return multiple_shows_metadata

    return []
