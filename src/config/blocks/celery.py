from pydantic import Field

from src.config.base import AppBaseSettings


class CelerySettings(AppBaseSettings):
    """Настройки Celery."""

    broker_url: str | None = Field(
        default=None,
        alias="CELERY_BROKER_URL"
    )
    result_backend: str | None = Field(
        default=None,
        alias="CELERY_RESULT_BACKEND"
    )
    task_always_eager: bool = Field(
        default=False,
        alias="CELERY_TASK_ALWAYS_EAGER"
    )
    job_repository_backend: str = Field(
        default="redis",
        alias="JOB_REPOSITORY_BACKEND",
    )

    def resolve_broker(self, redis_url: str) -> str:
        return self.broker_url or redis_url

    def resolve_result_backend(self, redis_url: str) -> str:
        return self.result_backend or redis_url
