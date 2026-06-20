"""Data ingestion and validation schemas for external TV Show API responses.

This module provides a single source of truth for structural validation of incoming
payloads from the external EpGuides service. It acts as an operational gateway,
ensuring that raw network dictionaries conform to expected data types and field
presence constraints before the data propagates further into the CLI or service layer.
"""

from pydantic import BaseModel, Field


class ShowSearchItem(BaseModel):
    """Parses individual show matches from the external API search array.

    Pydantic model will strip out uncessary fields such as country, start_date
    and URL fields are omitted entirely during parsing.
    """

    epguides_key: str = Field(..., description="The unique string key token identifying the show.")
    title: str = Field(..., description="The official name of the TV show.")
    network: str = Field(..., description="The broadcast network provider.")

    model_config = {
        # This explicit setting ensures unwanted fields are dropped silently
        "extra": "ignore"
    }


class ShowMetadataDetail(BaseModel):
    """Schema for the comprehensive metadata payload of a single specific show.

    Parses structural details from Endpoint A using an 'epguides_key' path parameter.
    """

    epguides_key: str
    title: str
    imdb_id: str
    network: str
    poster_url: str

    model_config = {"extra": "ignore"}


class ShowSeasonEpisodes(BaseModel):
    """Schema for the comprehensive metadata payload of a season of a specific show.

    Parses structural details to return a List of details such as episode name.
    """

    number: int = Field(..., description="Episode number in the season")
    season: int = Field(..., description="TV show season")
    title: str = Field(..., description="Title name of the episode")

    model_config = {"extra": "ignore"}
