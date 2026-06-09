from src.domain.enums import PipelineStage
from src.domain.entities import StageResult, PipelineContext
from src.application.ports.output import CatalogLoaderPort

from .base import PipelineStageHandler


class LoadDocumentStage(PipelineStageHandler):

    def __init__(self, loader: CatalogLoaderPort) -> None:
        self._loader = loader

    async def execute(self, context: PipelineContext) -> StageResult:
        source_path = context.job.metadata["source_path"]
        pages = self._loader.load(source_path)
        context.pages = pages

        return StageResult(
            stage=PipelineStage.LOAD_DOCUMENT,
            success=True,
            message=f"Loaded {len(pages)} pages",
        )
