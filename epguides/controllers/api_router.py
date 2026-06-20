"""API controller handling television show data routing.

This module encapsulates all JSON-based REST endpoints for the television show
domain, acting as the Controller layer in the MVC architecture.
"""

from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Path, Query

from epguides.schemas.shows import ShowMetadataDetail, ShowSearchItem, ShowSeasonEpisodes
from epguides.services.client import ShowAPIClient

router = APIRouter()

show_client = ShowAPIClient()


@router.get("/shows/search", summary="🔍 Search shows", response_model=list[ShowSearchItem])
def search_shows(
    query: str = Query(..., description="The name of the TV show to search for."),
    network: Optional[str] = Query(
        None,
        description="Optional TV Network filter (e.g., 'HBO', 'CW', 'Paramount')",
    ),
) -> list[Any]:
    """Queries external TV index and optional filters results by network.

    Args:
        query: String fragment of the target TV series title.
        network: Optional broadcast or streaming network filter

    Returns:
        List of sanitized, structured ShowSearchItem objects.
    """
    shows: list[ShowSearchItem] = show_client.search_shows(query=query)

    if network is not None:
        shows = [show for show in shows if show.network.lower() == network.lower()]

    return shows


@router.get("/show/metadata/{epguides_key}", summary="📺 Get show metadata", response_model=ShowMetadataDetail)
def get_show_metadata(epguides_key: str = Path(..., description="The exact epguides key")) -> Any:
    """Queries external TV index and optional filters results by network.

    Args:
        query: String fragment of the target TV series title.
        network: Optional broadcast or streaming network filter

    Returns:
        Dictionary of sanitized, structured ShowMetadataDetail objects.
    """
    show_metadata = show_client.fetch_show_metadata(epguides_key=epguides_key)

    if not show_metadata:
        raise HTTPException(status_code=404, detail="Metadata not found. No TV show matches the key.")

    return show_metadata


@router.get(
    "/show/{epguides_key}/seasons/{season_number}/episodes",
    summary="📋 Get season episodes",
    response_model=list[ShowSeasonEpisodes],
)
def get_season_episodes(
    epguides_key: str = Path(..., description="The unique EpGuides key for the show."),
    season_number: int = Path(..., description="The target season number.", ge=1),
) -> list[ShowSeasonEpisodes]:
    """Get all episodes for a specific season."""
    season_episodes = show_client.fetch_season_metadata(epguides_key=epguides_key, season_num=season_number)

    return season_episodes
