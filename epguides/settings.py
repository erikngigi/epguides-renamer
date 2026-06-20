"""Configuration module for the Show Management Service application.

This module loads, validates, and manages the application settings,
including the Uvicorn server deployment configurations and external API
endpoint connections. It exports a singleton `settings` object for
application-wide usage.
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Dynamically locate the absolute path to your project root
# This ensures nested directories can find the .env file
ROOT_DIR = Path(__file__).resolve().parent.parent


class AppConfig(BaseSettings):
    """Application-wide configuration settings and environmental variables.

    This class utilizes Pydantic to validate data types for server
    deployment settings and external service routing.

    Attributes:
        host (str): The network interface address the Uvicorn server
            binds to. Defaults to "127.0.0.1" (localhost).
        port (int): The network port the Uvicorn server listens on.
            Defaults to 8000.
        base_api_url (str): The base target URL of the external
            third-party API service.
        shows_endpoint (str): The specific relative path/route for
            fetching television show data.
    """

    host: str = "127.0.0.1"
    port: int = 8000

    epguides_show_url: str
    search_shows_endpoint: str

    model_config = SettingsConfigDict(env_file=ROOT_DIR / ".env", env_file_encoding="utf-8", extra="ignore")


settings = AppConfig()
