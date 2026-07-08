from src.utils import ProductData
from src.domain.enums import PipelineStage
from src.domain.entities import Product, StageResult, PipelineContext
from src.application.ports.output import TranslatorPort

from .base import PipelineStageHandler


class TranslateProductsStage(PipelineStageHandler):

    def __init__(self, translator: TranslatorPort) -> None:
        self._translator = translator

    @property
    def stage(self) -> PipelineStage:
        return PipelineStage.TRANSLATE_PRODUCTS

    async def execute(self, context: PipelineContext) -> StageResult:
        products = context.extracted_products or []

        translated_raw: list[ProductData] = await self._translator.translate(
            [p.to_dict() for p in products]
        )
        context.translated_products = [
            Product.from_dict(
                data,
                page_number=original.page_number,
            )
            for original, data in zip(products, translated_raw)
        ]

        return StageResult(
            stage=self.stage,
            success=True,
        )
