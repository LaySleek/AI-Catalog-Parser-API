from pydantic import Field

from src.config.base import AppBaseSettings


class VllmSettings(AppBaseSettings):
    """Настройки подключения к vLLM."""

    base_url: str = Field(
        default="http://vllm:8000/v1",
        alias="VLLM_BASE_URL"
    )
    api_key: str = Field(
        default="EMPTY",
        alias="VLLM_API_KEY",
    )
    timeout_sec: int = Field(
        default=300,
        alias="VLLM_TIMEOUT_SEC",
    )
    max_retries: int = Field(
        default=3,
        alias="VLLM_MAX_RETRIES",
    )
