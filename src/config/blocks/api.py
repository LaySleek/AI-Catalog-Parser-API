from pydantic import Field

from src.config.base import AppBaseSettings


class ApiSettings(AppBaseSettings):
    """Настройки API."""

    host: str = Field(
        default="0.0.0.0",
        alias="API_HOST"
    )
    port: int = Field(
        default=8000,
        alias="API_PORT"
    )
