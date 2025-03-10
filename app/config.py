from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic.types import DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL, AsyncAdaptedQueuePool

project_path: DirectoryPath = Path(__file__).parent.parent


class ApplicationSettings(BaseSettings):
    """Application related settings."""

    client_id: str | None = None
    client_secret: str | None = None


class RedisSettings(BaseSettings):
    """Redis related settings."""

    dsn: str | None = None
    use_fake_redis: bool | None = None


class TaskiqSettings(BaseSettings):
    """Taskiq related settings."""

    broker_url: str | None = None
    result_backend: str | None = None


class DatabaseSettings(BaseSettings):
    """Database related settings."""

    db_host: str | None = None
    db_port: int | None = None
    db_name: str | None = None
    db_username: str | None = None
    db_password: str | None = None

    pool_size: int = 10
    pool_pre_ping: bool = True
    connect_args: dict[str, Any] = {
        "prepare_threshold": None,
    }

    @property
    def uri(self) -> URL:
        """Fill up database uri."""

        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.db_username,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        )

    @property
    def engine_kwargs(self) -> dict[str, Any]:
        return {
            "pool_size": self.pool_size,
            "pool_pre_ping": self.pool_pre_ping,
            "connect_args": self.connect_args,
            "poolclass": AsyncAdaptedQueuePool,
        }


class Settings(BaseSettings):
    """Project settings."""

    application: ApplicationSettings
    redis: RedisSettings
    taskiq: TaskiqSettings
    database: DatabaseSettings
    project_path: DirectoryPath = project_path

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        env_nested_delimiter="__",
        extra="allow",
    )


@lru_cache
def get_settings() -> Settings:
    """Return all project settings."""

    return Settings()  # noqa
