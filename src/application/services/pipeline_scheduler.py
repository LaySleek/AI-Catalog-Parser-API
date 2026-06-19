from src.domain.services import ImageMatchingService
from src.application.pipeline import Pipeline
from src.application.ports.output import (
    TranslatorPort,
    ImageStoragePort,
    CatalogLoaderPort,
    LayoutDetectorPort,
    ProductExtractorPort,
    NomenclatureExporterPort
)
from src.application.pipeline.stages import (
    CropImagesStage,
    MatchImagesStage,
    DetectLayoutStage,
    LoadDocumentStage,
    ExtractProductsStage,
    TranslateProductsStage,
    ExportNomenclatureStage
)


class PipelineScheduler:

    def __init__(
        self,
        loader: CatalogLoaderPort,
        extractor: ProductExtractorPort,
        detector: LayoutDetectorPort,
        translator: TranslatorPort,
        image_storage: ImageStoragePort,
        exporter: NomenclatureExporterPort,
        matcher: ImageMatchingService | None = None,
    ) -> None:
        """Собирает стадии пайплайна в правильном порядке.

        Parameters
        ----------
        loader : CatalogLoaderPort
            Адаптер загрузчика каталогов.
        extractor : ProductExtractorPort
            Адаптер экстрактора карточек товаров.
        detector : LayoutDetectorPort
            Адаптер детектора изображений на странице каталога.
        translator : TranslatorPort
            Адаптер переводчика.
        image_storage : ImageStoragePort
            Адаптер хранилища изображений.
        exporter : NomenclatureExporterPort
            Адаптер экспортера номенклатур.
        matcher : ImageMatchingService | None, optional
            Сервис для сопоставления товаров с их bbox
            на странице каталога, by default None
        """
        self._matcher = matcher or ImageMatchingService()
        self._pipeline = Pipeline(
            stages=[
                LoadDocumentStage(loader),
                ExtractProductsStage(extractor),
                TranslateProductsStage(translator),
                DetectLayoutStage(detector),
                MatchImagesStage(self._matcher),
                CropImagesStage(image_storage),
                ExportNomenclatureStage(exporter),
            ]
        )

    @property
    def pipeline(self) -> Pipeline:
        return self._pipeline
