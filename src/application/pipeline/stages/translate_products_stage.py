from src.utils import ProductData
from src.domain.enums import PipelineStage
from src.domain.entities import Product, StageResult, PipelineContext
from src.application.ports.output import TranslatorPort

from .base import PipelineStageHandler


class TranslateProductsStage(PipelineStageHandler):

    def __init__(self, translator: TranslatorPort) -> None:
        self._translator = translator

    async def execute(self, context: PipelineContext) -> StageResult:
        products = context.extracted_products or []

        translated_raw: list[ProductData] = self._translator.translate(
            [p.to_dict() for p in products]
        )
        context.translated_products = [
            Product.from_dict(
                data,
                page_number=data.get("page_number"),
            )
            for data in translated_raw
        ]

        return StageResult(
            stage=PipelineStage.TRANSLATE_PRODUCTS,
            success=True,
        )
