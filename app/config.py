from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    email: str = "sample@email.com"

    model_config = SettingsConfigDict(env_file="../.env")


@lru_cache
def get_settings() -> BaseSettings:
    return _Settings()
