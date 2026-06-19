from pydantic import Field

from src.config.base import AppBaseSettings


class RedisSettings(AppBaseSettings):
    """Настройки Redis."""

    url: str = Field(
        default="redis://localhost:6379/0",
        alias="REDIS_URL"
    )
