from src.domain.entities import PipelineContext

from .stages import PipelineStageHandler


class Pipeline:

    def __init__(self, stages: list[PipelineStageHandler]) -> None:
        self._stages = stages

    async def run(self, context: PipelineContext) -> PipelineContext:
        for stage in self._stages:
            await stage.execute(context)

        return context
