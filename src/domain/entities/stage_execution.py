from datetime import UTC, datetime
from dataclasses import field, dataclass

from src.domain.enums import JobStatus, PipelineStage


@dataclass(slots=True, kw_only=True)
class StageExecution:
    stage: PipelineStage
    status: JobStatus

    error: str | None = None
    retry_count: int = 0
    worker_id: str | None = None
    duration_seconds: float | None = None

    started_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )
    finished_at: datetime | None = None
