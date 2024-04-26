from functools import lru_cache  # For caching function results to improve performance

from pydantic_settings import (  # Pydantic base class for settings management
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    """
    Application settings for the FastAPI project.

    This class uses Pydantic to define application-specific settings,
    with values provided from environment variables or default values.
    """

    app_name: str = "CyberHQ API"  # Default application name
    jwt_algorithm: str = "HS256"  # Algorithm used for JWT tokens
    jwt_secret: str  # Secret key for signing JWT tokens
    jwt_expiration: int = 30  # Token expiration time in minutes

    # Configuration for loading environment variables from a specific file
    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()  # Caches the result to avoid redundant computations
def get_settings():
    """
    Fetches the application settings, utilizing caching to improve performance.

    This function retrieves the settings defined in the `Settings` class,
    caching the result for efficiency. This is typically used with FastAPI's
    dependency injection.
    """
    return Settings()  # Return an instance of the Settings class
