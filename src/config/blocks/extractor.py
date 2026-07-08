from pydantic import Field

from src.config.base import AppBaseSettings


class ExtractorSettings(AppBaseSettings):
    """Настройки модели извлечения карточек товаров."""

    model_id: str = Field(
        default="numind/NuExtract3",
        alias="EXTRACTOR_MODEL_ID",
    )
    enable_thinking: bool = Field(
        default=True,
        alias="EXTRACTOR_ENABLE_THINKING"
    )
    max_new_tokens: int | None = Field(
        default=None,
        ge=1,
        alias="EXTRACTOR_MAX_NEW_TOKENS"
    )
    page_batch_size: int = Field(
        default=1,
        ge=1,
        alias="EXTRACTOR_PAGE_BATCH_SIZE",
    )
