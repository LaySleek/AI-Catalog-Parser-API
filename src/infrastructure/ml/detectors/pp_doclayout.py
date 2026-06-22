import torch

from src.utils import chunked
from src.domain.enums import PreprocessProfile
from src.config.settings import Settings, get_settings
from src.domain.entities import BBox, CatalogPage
from src.domain.exceptions import LayoutDetectionError
from src.infrastructure.ml.registry.model_registry import ModelRegistry
from src.infrastructure.ml.preprocessors.image_preprocessor import ImagePreprocessor


class PPDocLayoutDetector:
    """Детектор bbox изображений через PP-DocLayoutV3."""

    def __init__(
        self,
        registry: ModelRegistry | None = None,
        preprocessor: ImagePreprocessor | None = None,
        settings: Settings | None = None,
    ) -> None:
        self._registry = registry or ModelRegistry.get()
        self._preprocessor = preprocessor or ImagePreprocessor()
        self._settings = settings or get_settings()
        self._detector = self._settings.detector

    def detect(
        self,
        pages: list[CatalogPage],
        *,
        profile: PreprocessProfile | None = None,
    ) -> list[list[BBox]]:

        if not pages:
            return []

        batch_results: list[list[BBox]] = []

        for page_batch in chunked(pages, self._detector.page_batch_size):
            batch_results.extend(
                self._detect_batch(page_batch, profile=profile)
            )

        return batch_results

    def _detect_batch(
        self,
        pages: list[CatalogPage],
        *,
        profile: PreprocessProfile | None = None,
    ) -> list[list[BBox]]:
        """Выполняет детекцию изображений на батче
        страниц каталога.

        Parameters
        ----------
        pages : list[CatalogPage]
            Список страниц каталога.
        profile : PreprocessProfile | None, optional
            Профиль предобработки изображений для детектора, by default None.

        Returns
        -------
        list[list[BBox]]
            Список bbox-ов для каждой страницы каталога.

        Raises
        ------
        LayoutDetectionError
            Если при предобработке для какой-то страницы произошла ошибка.
        """
        preprocessed = [
            self._preprocessor.preprocess_for_detection(
                self._preprocessor.page_to_pil(page),
                profile=profile,
            )
            for page in pages
        ]

        processor = self._registry.detector_processor
        model = self._registry.detector

        try:
            inputs = processor(
                images=preprocessed,
                return_tensors="pt",
            ).to(model.device)

        except Exception as exc:
            page_number = pages[0].page_number if pages else 0

            raise LayoutDetectionError(
                page_number=page_number,
                reason=str(exc)
            ) from exc

        with torch.inference_mode():
            outputs = model(**inputs)

        detector_results = processor.post_process_object_detection(
            outputs,
            threshold=self._detector.detection_threshold,
            target_sizes=[img.size[::-1] for img in preprocessed],
        )

        batch_results: list[list[BBox]] = []
        for result in detector_results:
            boxes = result["boxes"]
            label_ids = result["labels"]
            page_bboxes: list[BBox] = []

            for bbox, label_id in zip(boxes, label_ids):
                label = model.config.id2label[label_id.item()]
                if label != "image":
                    continue

                page_bboxes.append(BBox.from_list(bbox.tolist()))

            batch_results.append(page_bboxes)

        return batch_results
