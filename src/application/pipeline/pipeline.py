from src.domain.entities import PipelineContext
from src.domain.exceptions import CatalogParserError

from .stages import PipelineStageHandler


class Pipeline:

    def __init__(self, stages: list[PipelineStageHandler]) -> None:
        self._stages = stages

    async def run(self, context: PipelineContext) -> PipelineContext:
        """Запускает задачу на обработку каталога.

        Последовательно запускает все стадии, из ``self._stages``,
        обновляя контекст задачи ``context`` после каждой стадии.

        Parameters
        ----------
        context : PipelineContext
            Контекст задачи на обработку каталога.

        Returns
        -------
        PipelineContext
            Контекст задачи, полученный после обработки всеми стадиями ``self._stages``.

        Raises
        ------
        CatalogParserError
            Если одна из стадий завершилась с ошибкой.
        """
        for stage in self._stages:
            context.job.start_stage(stage.stage)
            result = await stage.execute(context)

            if not result.success:
                message = result.message or f"Stage {result.stage} failed"
                raise CatalogParserError(message)

        context.job.complete()
        return context
