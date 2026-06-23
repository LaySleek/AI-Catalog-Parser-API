from .config import Settings, get_settings
from .domain.services import ImageMatchingService
from .application.handlers import ProcessCatalogHandler
from .application.pipeline import Pipeline
from .application.services import PipelineScheduler
from .infrastructure.storage import (
    LocalImageStorage,
    RedisJobRepository,
    ExcelNomenclatureExporter
)
from .infrastructure.document import LoaderFactory
from .application.ports.output import JobRepositoryPort
from .infrastructure.ml.detectors import PPDocLayoutDetector
from .infrastructure.ml.extractors import NuExtractExtractor
from .infrastructure.ml.translators import NuExtractTranslator


def build_pipeline(settings: Settings | None = None) -> Pipeline:
    settings = settings or get_settings()
    scheduler = PipelineScheduler(
        loader=LoaderFactory(settings),
        extractor=NuExtractExtractor(settings),
        translator=NuExtractTranslator(settings),
        detector=PPDocLayoutDetector(settings),
        image_storage=LocalImageStorage(settings),
        exporter=ExcelNomenclatureExporter(settings),
        matcher=ImageMatchingService(),
    )
    return scheduler.pipeline


def build_job_repository(settings: Settings | None = None) -> JobRepositoryPort:
    settings = settings or get_settings()
    return RedisJobRepository(settings)


def create_process_handler(settings: Settings | None = None) -> ProcessCatalogHandler:
    settings = settings or get_settings()
    return ProcessCatalogHandler(
        pipeline=build_pipeline(settings),
        job_repository=build_job_repository(settings),
        settings=settings,
    )
