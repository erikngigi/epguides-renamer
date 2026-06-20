"""Specialized resource clients for interacting with distinct API domains."""

from typing import Any, Dict, Optional, cast

import httpx
from fastapi import HTTPException

from epguides.schemas.shows import ShowMetadataDetail, ShowSearchItem, ShowSeasonEpisodes
from epguides.services.base_client import BaseAPIClient
from epguides.settings import settings


class ShowAPIClient(BaseAPIClient):
    """Client for managing operations related to the /shows endpoint."""

    def __init__(self) -> None:
        # Call the parent class __init__ and pass the global base URL
        super().__init__(base_url=settings.epguides_show_url)
        # Define this client's unique path
        self.target_url = f"{self.base_url}"

    def fetch_shows(self, page: int = 1, limit: int = 100) -> list[ShowSearchItem]:
        """Fetches a paginated list of shows validated as Pydantic objects.

        Raises:
            HTTPException: If an upstream network or service error occurs.
        """
        params = {"page": page, "limit": limit}
        try:
            response = self.client.get(self.target_url, params=params)
            response.raise_for_status()

            raw_data = response.json()
            return [ShowSearchItem(**item) for item in raw_data]
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=f"Upsteam API pagination fetch failed: {exc}")

    def search_shows(self, query: str) -> list[ShowSearchItem]:
        """Searches for a specific TV show by its name string fragment.

        Args:
            query (str): The search phrase or title piece of the target show.

        Returns:
            List[ShowSearchItem]: A clean sequence of structured, validated shows.

        Raises:
            HTTPException: If the upstream service disconnects or returns bad data.
        """
        search_url = f"{self.target_url.rstrip('/')}/{settings.search_shows_endpoint}"
        params: dict[str, Any] = {"query": query}

        try:
            response = self.client.get(search_url, params=params)
            response.raise_for_status()

            raw_data = response.json()

            # Boundary guard: handling cases where the API returns an unexpected data layout
            if not isinstance(raw_data, list):
                raise HTTPException(
                    status_code=502, detail="Upstream API returned an invalid data format (expected and array)."
                )

            return [ShowSearchItem(**item) for item in raw_data]

        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=f"Upstream network search endpoint failed: {exc}")

    def fetch_show_metadata(self, epguides_key: str) -> ShowMetadataDetail:
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

            return ShowMetadataDetail(**response.json())

        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=f"Upstream metadata lookup failed for '{epguides_key}': {exc}")

    def fetch_season_metadata(self, epguides_key: str, season_num: int) -> list[ShowSeasonEpisodes]:
        """Fetches the season metadata of a specific TV Show using the epguides_key and a optional season params.

        Args:
            epguides_key (str): The key of the target show.
            season_num (int): The season of the target show.

        Returns:
            list[Any]: A list of the matched TV show seasonal episode metadata if successful.
        """
        search_url = f"{self.target_url.rstrip('/')}/{epguides_key}/seasons/{season_num}/episodes"

        params: dict[str, Any] = {"epguides_key": epguides_key, "season_num": season_num}

        try:
            response = self.client.get(search_url, params=params)
            response.raise_for_status()

            raw_data = response.json()

            # Boundary guard: handling cases where the API returns an unexpected data layout
            if not isinstance(raw_data, list):
                raise HTTPException(
                    status_code=502, detail="Upstream API returned an invalid data format (expected and array)."
                )

            return [ShowSeasonEpisodes(**item) for item in raw_data]

        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=f"Upstream season_number search endpoint failed: {exc}")
