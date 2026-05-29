from uuid import UUID, uuid4
from typing import Any
from datetime import UTC, datetime
from dataclasses import field, dataclass

from src.domain.enums import JobStatus, PipelineStage

from .pipeline_artifact import PipelineArtifact


@dataclass(slots=True, kw_only=True)
class PipelineJob:
    """Задача пайплайна.

    Attributes
    ----------
    id : UUID, optional
        Идентификатор задачи, by default uuid4.
    status : JobStatus, optional
        Текущий статус пайплайна, by default JobStatus.PENDING.
    current_stage : PipelineStage | None, optional
        Текущая выполняемая стадия, by default None.
    artifacts : list[PipelineArtifact], optional
        Артефакты пайплайна, by default [].
    metadata : dict[str, Any], optional
        Метаданные задачи, by default {}.
    errors : list[str], optional
        Ошибки пайплайна, by default [].
    created_at : datetime, optional
        Время создания задачи, by default datetime.now(UTC).
    updated_at : datetime, optional
        Время обновления задачи, by default datetime.now(UTC).
    started_at : datetime, optional
        Время начала выполнения задачи, by default None.
    finished_at : datetime, optional
        Время окончания выполнения задачи, by default None.
    retry_count : int, optional
        Текущее количество перезапусков данной задачи, by default 0.
    """
    id: UUID = field(default_factory=uuid4)

    status: JobStatus = JobStatus.PENDING
    current_stage: PipelineStage | None = None
    artifacts: list[PipelineArtifact] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )
    started_at: datetime | None = None
    finished_at: datetime | None = None

    retry_count: int = 0

    def start_stage(self, stage: PipelineStage) -> None:
        self.current_stage = stage
        self.status = JobStatus.RUNNING

        if self.started_at is None:
            self.started_at = datetime.now(UTC)

        self.update()

    def complete(self) -> None:
        self.status = JobStatus.COMPLETED
        self.finished_at = datetime.now(UTC)

        self.update()

    def fail(self, error: str) -> None:
        self.status = JobStatus.FAILED
        self.errors.append(error)
        self.finished_at = datetime.now(UTC)

        self.update()

    def add_artifact(self, artifact: PipelineArtifact) -> None:
        self.artifacts.append(artifact)
        self.update()

    def update(self) -> None:
        self.updated_at = datetime.now(UTC)
