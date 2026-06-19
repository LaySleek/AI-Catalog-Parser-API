from src.utils import ProductData
from src.domain.enums import PipelineStage
from src.domain.entities import Product, StageResult, PipelineContext
from src.application.ports.output import ProductExtractorPort

from .base import PipelineStageHandler


class ExtractProductsStage(PipelineStageHandler):

    def __init__(self, extractor: ProductExtractorPort) -> None:
        self._extractor = extractor

    @property
    def stage(self) -> PipelineStage:
        return PipelineStage.EXTRACT_PRODUCTS

    async def execute(self, context: PipelineContext) -> StageResult:
        pages = context.pages or []

        per_page_data: list[list[ProductData]] = self._extractor.extract(pages)

        products: list[Product] = []
        parse_errors: list[str] = []

        for page, page_data in zip(pages, per_page_data):
            for raw in page_data:
                try:
                    product = Product.from_dict(
                        raw,
                        page_number=page.page_number,
                    )
                    products.append(product)
                except (ValueError, KeyError) as exc:
                    sku = raw.get("sku", "<unknown>")
                    parse_errors.append(
                        f"page {page.page_number}, sku={sku!r}: {exc}"
                    )

        context.extracted_products = products

        message = (
            f"Extracted {len(products)} products "
            f"from {len(pages)} pages"
            + (f"; skipped {len(parse_errors)}" if parse_errors else "")
        )

        return StageResult(
            stage=self.stage,
            success=True,
            message=message,
            errors=parse_errors,
        )
