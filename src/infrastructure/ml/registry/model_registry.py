import threading

from transformers import AutoImageProcessor, AutoModelForObjectDetection

from src.config.settings import Settings, get_settings


class ModelRegistry:
    """Singleton с ленивой загрузкой моделей."""

    _instance: "ModelRegistry | None" = None
    _lock = threading.Lock()

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._detector = None
        self._detector_processor = None
        self._detector_lock = threading.Lock()

    @classmethod
    def get(cls, settings: Settings | None = None) -> "ModelRegistry":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls(settings)
        return cls._instance

    @property
    def detector(self):
        self._ensure_detector()
        return self._detector

    @property
    def detector_processor(self):
        self._ensure_detector()
        return self._detector_processor

    def warmup(self) -> None:
        """Инициализация всех моделей."""
        self._ensure_detector()

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
