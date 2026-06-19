from src.domain.enums import PipelineStage
from src.domain.entities import StageResult, PipelineContext
from src.application.ports.output import LayoutDetectorPort

from .base import PipelineStageHandler


class DetectLayoutStage(PipelineStageHandler):

    def __init__(self, detector: LayoutDetectorPort) -> None:
        self._detector = detector

    @property
    def stage(self) -> PipelineStage:
        return PipelineStage.DETECT_LAYOUT

    async def execute(self, context: PipelineContext) -> StageResult:
        pages = context.pages or []
        context.detections = self._detector.detect(
            pages,
            profile=context.preprocess_profile,
        )

        return StageResult(
            stage=self.stage,
            success=True,
        )
