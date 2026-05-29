from dataclasses import dataclass

from .bbox import BBox
from .page import CatalogPage
from .product import Product
from .pipeline_job import PipelineJob


@dataclass(slots=True)
class PipelineContext:
    job: PipelineJob

    pages: list[CatalogPage] | None = None

    extracted_products: list[Product] | None = None
    translated_products: list[Product] | None = None
    detections: list[list[BBox]] | None = None
