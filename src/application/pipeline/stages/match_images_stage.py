from collections import defaultdict

from src.domain.enums import PipelineStage
from src.domain.entities import BBox, Product, StageResult, PipelineContext
from src.domain.services import ImageMatchingService

from .base import PipelineStageHandler


class MatchImagesStage(PipelineStageHandler):

    def __init__(self, matcher: ImageMatchingService) -> None:
        self._matcher = matcher

    @property
    def stage(self) -> PipelineStage:
        return PipelineStage.MATCH_IMAGES

    async def execute(self, context: PipelineContext) -> StageResult:
        products = context.translated_products or []
        pages = context.pages or []
        detections = context.detections or []

        products_by_page: dict[int, list[Product]] = defaultdict(list)
        for product in products:
            products_by_page[product.page_number].append(product)

        matches: list[tuple[Product, BBox]] = []
        for page, page_bboxes in zip(pages, detections):
            page_products = products_by_page.get(page.page_number, [])

            matches.extend(
                self._matcher.match(
                    page=page,
                    products=page_products,
                    bboxes=page_bboxes,
                )
            )

        context.matches = matches

        return StageResult(
            stage=self.stage,
            success=True,
        )
