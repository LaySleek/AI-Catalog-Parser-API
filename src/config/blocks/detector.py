from pydantic import Field

from src.config.base import AppBaseSettings
from src.config.mixins import TorchDtypeMixin


class DetectorSettings(TorchDtypeMixin, AppBaseSettings):
    """Настройки модели детекции изображений на странице каталога."""

    model_device: str = Field(
        default="auto",
        alias="MODEL_DEVICE"
    )
    model_id: str = Field(
        default="PaddlePaddle/PP-DocLayoutV3_safetensors",
        alias="DETECTOR_MODEL_ID",
    )
    detection_threshold: float = Field(
        default=0.3,
        ge=0.0,
        alias="DETECTOR_DETECTION_THRESHOLD",
    )
    page_batch_size: int = Field(
        default=1,
        ge=1,
        alias="DETECTOR_PAGE_BATCH_SIZE",
    )
