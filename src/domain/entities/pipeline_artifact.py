from uuid import UUID, uuid4
from typing import Any
from pathlib import Path
from datetime import UTC, datetime
from dataclasses import field, dataclass

from src.domain.enums import ArtifactType, PipelineStage


@dataclass(slots=True, kw_only=True)
class PipelineArtifact:
    """Артефакт, созданный на этапе пайплайна.

    Attributes
    ----------
    artifact_type : ArtifactType
        Тип артефакта.
    stage : PipelineStage
        Cтадия пайплайна, создавшая артефакт.
    path : Path
        Путь до артефакта в бэкенде хранилища.
    id : UUID, optional
        Уникальный идентификатор артефакта, by default uuid4.
    metadata : dict[str, Any], optional
        Дополнительные метаданные, by default {}.
    created_at : datetime, optional
        Время создания артефакта, by default datetime.now(UTC).
    """
    artifact_type: ArtifactType
    stage: PipelineStage
    path: Path

    id: UUID = field(default_factory=uuid4)

    metadata: dict[str, Any] = field(default_factory=dict)

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    @property
    def filename(self) -> str:
        return self.path.name

    @property
    def exists(self) -> bool:
        return self.path.exists()
