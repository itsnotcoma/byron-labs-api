from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CyberHQ API"
    jwt_algorithm: str = "HS256"
    jwt_secret: str
    jwt_expiration: int = 30  # minutes

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings():
    return Settings()
