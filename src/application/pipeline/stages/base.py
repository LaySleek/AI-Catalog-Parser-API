from abc import ABC, abstractmethod

from src.domain.entities import StageResult, PipelineContext


class PipelineStageHandler(ABC):

    @abstractmethod
    async def execute(self, context: PipelineContext) -> StageResult:
        ...
