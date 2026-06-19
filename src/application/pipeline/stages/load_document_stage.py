from pathlib import Path

from src.domain.enums import PipelineStage, PreprocessProfile
from src.domain.entities import StageResult, PipelineContext
from src.application.ports.output import CatalogLoaderPort

from .base import PipelineStageHandler


class LoadDocumentStage(PipelineStageHandler):

    def __init__(self, loader: CatalogLoaderPort) -> None:
        self._loader = loader

    @property
    def stage(self) -> PipelineStage:
        return PipelineStage.LOAD_DOCUMENT

    async def execute(self, context: PipelineContext) -> StageResult:
        source_path = Path(context.job.metadata["source_path"])
        pages = self._loader.load(source_path)
        context.pages = pages

        profile_raw = context.job.metadata.get("profile")
        if profile_raw is not None:
            context.preprocess_profile = PreprocessProfile(profile_raw)

        elif context.job.metadata.get("preprocess_profile") is not None:
            context.preprocess_profile = PreprocessProfile(
                context.job.metadata["preprocess_profile"]
            )

        return StageResult(
            stage=self.stage,
            success=True,
            message=f"Loaded {len(pages)} pages",
        )
