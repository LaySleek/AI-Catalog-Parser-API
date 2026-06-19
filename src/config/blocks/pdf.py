from pydantic import Field

from src.config.base import AppBaseSettings


class PdfSettings(AppBaseSettings):
    """Настройки конвертации PDF в изображения."""

    render_dpi: int = Field(
        default=200,
        ge=1,
        alias="PDF_RENDER_DPI"
    )
