from src.domain.enums import PipelineStage
from src.domain.entities import StageResult, PipelineContext
from src.application.ports.output import ImageStoragePort

from .base import PipelineStageHandler


class CropImagesStage(PipelineStageHandler):

    def __init__(self, storage: ImageStoragePort) -> None:
        self._storage = storage

    @property
    def stage(self) -> PipelineStage:
        return PipelineStage.CROP_IMAGES

    async def execute(self, context: PipelineContext) -> StageResult:
        pages = {
            p.page_number: p
            for p in context.pages or []
        }
        matches = context.matches or []

        for product, bbox in matches:
            page = pages[product.page_number]

            product.image_path = self._storage.save_crop(
                page=page,
                bbox=bbox,
                name=f"{product.name}_{product.sku}",
            )

        return StageResult(
            stage=self.stage,
            success=True,
        )
