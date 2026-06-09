from dataclasses import dataclass

from src.domain.enums import PipelineStage


@dataclass(slots=True, frozen=True)
class StageResult:
    """
    Результат выполнения стадии пайплайна.

    Attributes
    ----------
    stage : PipelineStage
        Выполненная стадия.
    success : bool
        Признак успешного выполнения.
    message : str | None
        Дополнительная информация.
    """
    stage: PipelineStage
    success: bool
    message: str | None = None
