from uuid import UUID

import redis

from src.config.settings import Settings, get_settings
from src.domain.entities import PipelineJob

from .job_serializer import serialize_job, deserialize_job


class RedisJobRepository:
    """Redis-хранилище статусов задач."""

    KEY_PREFIX = "catalog-parser:job:"

    def __init__(
        self,
        settings: Settings | None = None,
        client: redis.Redis | None = None,
    ) -> None:
        self._settings = settings or get_settings()
        self._client = client or redis.from_url(
            self._settings.redis.url,
            decode_responses=True,
        )

    def save(self, job: PipelineJob) -> None:
        self._client.set(self._key(job.id), serialize_job(job))

    def get(self, job_id: UUID) -> PipelineJob | None:
        payload = self._client.get(self._key(job_id))
        if payload is None:
            return None
        return deserialize_job(payload)

    def _key(self, job_id: UUID) -> str:
        return f"{self.KEY_PREFIX}{job_id}"
