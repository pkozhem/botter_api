from functools import lru_cache
from pathlib import Path

from pydantic import RedisDsn
from pydantic.types import DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import AsyncAdaptedQueuePool, URL

PROJECT_PATH: DirectoryPath = Path(__file__).parent.parent


class _ApplicationSettings(BaseSettings):
    CLIENT_ID: str = ""
    CLIENT_SECRET: str = ""


class _DatabaseSettings(BaseSettings):
    DB_HOST: str = ""
    DB_PORT: int = ""
    DB_NAME: str = ""
    DB_USERNAME: str = ""
    DB_PASSWORD: str = ""
    DB_DRIVER_NAME: str = ""
    DB_POOL_SIZE: int = 10

    @property
    def uri(self) -> URL:
        """URI for database connection."""

        return URL.create(
            drivername=self.DB_DRIVER_NAME,
            username=self.DB_USERNAME,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        )

    @property
    def engine_kwargs(self):
        return {
            "pool_size": self.DB_POOL_SIZE,
            "pool_use_lifo": True,
            "pool_pre_ping": True,
            "connect_args": {
                "prepare_threshold": None,
            },
            "poolclass": AsyncAdaptedQueuePool,
        }


class _RedisSettings(BaseSettings):
    DSN: RedisDsn | None = None
    USE_FAKE_REDIS: bool = False
    SOCKET_CONNECT_TIMEOUT: int = 5
    RETRY_ON_TIMEOUT: bool = True
    SOCKET_KEEPALIVE: bool = True


class _TaskiqSettings(BaseSettings):
    BROKER_URL: str = ""
    RESULT_BACKEND: str = ""


class Settings(BaseSettings):
    PROJECT_PATH: DirectoryPath = PROJECT_PATH
    APPLICATION: _ApplicationSettings = _ApplicationSettings()
    DATABASE: _DatabaseSettings = _DatabaseSettings()
    REDIS: _RedisSettings = _RedisSettings()
    TASKIQ: _TaskiqSettings = _TaskiqSettings()

    model_config = SettingsConfigDict(
        env_file="../.env",
        case_sensitive=True,
        env_prefix="",
        env_nested_delimiter="__",
        extra="allow",
    )


@lru_cache
def get_settings() -> BaseSettings:
    return Settings()
