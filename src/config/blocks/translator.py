from pydantic import Field

from src.config.base import AppBaseSettings
from src.config.mixins import TorchDtypeMixin


class TranslatorSettings(TorchDtypeMixin, AppBaseSettings):
    """Настройки модели перевода."""

    model_device: str = Field(
        default="auto",
        alias="MODEL_DEVICE"
    )
    model_id: str = Field(
        default="numind/NuExtract3",
        alias="TRANSLATOR_MODEL_ID"
    )
    enable_thinking: bool = Field(
        default=True,
        alias="TRANSLATOR_ENABLE_THINKING"
    )
    max_new_tokens: int = Field(
        default=4096,
        alias="TRANSLATOR_MAX_NEW_TOKENS"
    )
    product_batch_size: int = Field(
        default=1,
        ge=1,
        alias="TRANSLATOR_PRODUCT_BATCH_SIZE",
    )
