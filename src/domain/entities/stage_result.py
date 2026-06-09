from dataclasses import field, dataclass

from src.domain.enums import PipelineStage


@dataclass(frozen=True, slots=True)
class StageResult:
    """Результат выполнения стадии пайплайна.

    Attributes
    ----------
    stage : PipelineStage
        Стадия пайплайна, вернувшая данный результат.
    success : bool
        Флаг успешного завершения стадии.
    message : str | None, optional
        Опциональное сообщение о результате выполнения, by default `None`.
    errors : list[str], optional
        Список некритических ошибок, не прерывающих пайплайн, by default `[]`.
    """
    stage: PipelineStage
    success: bool
    message: str | None = None
    errors: list[str] = field(default_factory=list)
