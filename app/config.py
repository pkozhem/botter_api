from functools import lru_cache
from pathlib import Path

from pydantic.types import DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

PROJECT_PATH: DirectoryPath = Path(__file__).parent.parent



class Settings(BaseSettings):
    DB_HOST: str | None = None
    DB_PORT: int | None = None
    DB_NAME: str | None = None
    DB_USERNAME: str | None = None
    DB_PASSWORD: str | None = None
    PROJECT_PATH: DirectoryPath = PROJECT_PATH

    model_config = SettingsConfigDict(
        env_file="../.env",
        case_sensitive=True,
        env_prefix="",
        env_nested_delimiter="__",
        extra="allow",
    )

    @property
    def DATABASE_URI(self):  # noqa
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.DB_USERNAME,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
