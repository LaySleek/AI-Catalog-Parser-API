import threading

from transformers import (
    AutoProcessor,
    AutoImageProcessor,
    AutoModelForImageTextToText,
    AutoModelForObjectDetection
)

from src.config.settings import Settings, get_settings


class ModelRegistry:
    """Singleton с ленивой загрузкой моделей."""

    _instance: "ModelRegistry | None" = None
    _lock = threading.Lock()

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._extractor = None
        self._extractor_processor = None
        self._translator = None
        self._translator_processor = None
        self._detector = None
        self._detector_processor = None

    @classmethod
    def get(cls, settings: Settings | None = None) -> "ModelRegistry":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls(settings)
        return cls._instance

    @property
    def extractor(self):
        self._ensure_extractor()
        return self._extractor

    @property
    def extractor_processor(self):
        self._ensure_extractor()
        return self._extractor_processor

    @property
    def translator(self):
        self._ensure_translator()
        return self._translator

    @property
    def translator_processor(self):
        self._ensure_translator()
        return self._translator_processor

    @property
    def detector(self):
        self._ensure_detector()
        return self._detector

    @property
    def detector_processor(self):
        self._ensure_detector()
        return self._detector_processor

    def _ensure_extractor(self) -> None:
        """
        Инициализирует модель экстрактора товаров из каталога,
        если она не была инициализирована ранее.
        """
        if self._extractor is not None:
            return

        model_id = self._settings.extractor.model_id
        self._extractor = AutoModelForImageTextToText.from_pretrained(
            model_id,
            dtype=self._settings.extractor.dtype,
            device_map=self._settings.extractor.model_device,
        ).eval()
        self._extractor_processor = AutoProcessor.from_pretrained(
            model_id,
            padding_side="left",
        )

    def _ensure_translator(self) -> None:
        """
        Инициализирует модель переводчика,
        если она не была инициализирована ранее.
        """
        if self._translator is not None:
            return

        model_id = self._settings.translator.model_id

        # Пропуск инициализации, если переводчик является той же
        # моделью, что и экстрактор
        if (
            self._extractor is not None
            and model_id == self._settings.extractor.model_id
        ):
            self._translator = self._extractor
            self._translator_processor = self._extractor_processor
            return

        self._translator = AutoModelForImageTextToText.from_pretrained(
            model_id,
            dtype=self._settings.translator.dtype,
            device_map=self._settings.translator.model_device,
        ).eval()
        self._translator_processor = AutoProcessor.from_pretrained(
            model_id,
            padding_side="left",
        )

    def _ensure_detector(self) -> None:
        """
        Инициализирует модель детектора изображений,
        если она не была инициализирована ранее.
        """
        if self._detector is not None:
            return

        model_id = self._settings.detector.model_id
        self._detector = AutoModelForObjectDetection.from_pretrained(
            model_id,
            device_map=self._settings.detector.model_device,
        ).eval()
        self._detector_processor = AutoImageProcessor.from_pretrained(model_id)
