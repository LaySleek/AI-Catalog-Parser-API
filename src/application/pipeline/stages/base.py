from abc import ABC, abstractmethod

from src.domain.enums import PipelineStage
from src.domain.entities import StageResult, PipelineContext


class PipelineStageHandler(ABC):

    @property
    @abstractmethod
    def stage(self) -> PipelineStage:
        """Возвращает название текущей стадии пайплайна.

        Returns
        -------
        PipelineStage
            Название стадии пайплайна.
        """
        ...

    @abstractmethod
    async def execute(self, context: PipelineContext) -> StageResult:
        """Выполняет одну стадию пайплайна обработки каталога с учетом
        текущего контекста задачи ``context``.

        Parameters
        ----------
        context : PipelineContext
            Контекст задачи обработки пайплайна.

        Returns
        -------
        StageResult
            Результат выполнения стадии.
        """
        ...
