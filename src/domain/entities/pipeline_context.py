from dataclasses import dataclass

from src.domain.enums import PreprocessProfile

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
    matches: list[tuple[Product, BBox]] | None = None
    preprocess_profile: PreprocessProfile | None = None
