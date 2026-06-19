from pathlib import Path

from src.domain.enums import ArtifactType, PipelineStage
from src.domain.entities import StageResult, PipelineContext, PipelineArtifact
from src.application.ports.output import NomenclatureExporterPort

from .base import PipelineStageHandler


class ExportNomenclatureStage(PipelineStageHandler):

    def __init__(self, exporter: NomenclatureExporterPort) -> None:
        self._exporter = exporter

    @property
    def stage(self) -> PipelineStage:
        return PipelineStage.EXPORT_NOMENCLATURE

    async def execute(self, context: PipelineContext) -> StageResult:
        products = context.translated_products or []
        output_path = Path(context.job.metadata["output_path"])

        export_path = self._exporter.export(products, output_path)

        context.job.add_artifact(
            PipelineArtifact(
                artifact_type=ArtifactType.NOMENCLATURE_EXPORT,
                stage=self.stage,
                path=export_path,
            )
        )

        return StageResult(
            stage=self.stage,
            success=True,
            message=f"Exported {len(products)} products to {export_path}",
        )
