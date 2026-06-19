from pathlib import Path

from src.domain.enums import CatalogFormat
from src.config.settings import Settings
from src.domain.entities import CatalogPage
from src.domain.exceptions import UnsupportedFormatError

from .loaders.pdf_loader import PDFLoader
from .loaders.pptx_loader import PptxLoader
from .loaders.word_loader import WordLoader
from .loaders.excel_loader import ExcelLoader
from .loaders.image_loader import ImageLoader


class LoaderFactory:
    """Выбирает загрузчик каталога по расширению файла."""

    _EXTENSIONS: dict[str, CatalogFormat] = {
        ".pdf": CatalogFormat.PDF,
        ".xlsx": CatalogFormat.EXCEL,
        ".xls": CatalogFormat.EXCEL,
        ".docx": CatalogFormat.WORD,
        ".pptx": CatalogFormat.POWERPOINT,
        ".png": CatalogFormat.IMAGE,
        ".jpg": CatalogFormat.IMAGE,
        ".jpeg": CatalogFormat.IMAGE,
    }

    def __init__(self, settings: Settings | None = None) -> None:
        self._loaders = {
            CatalogFormat.PDF: PDFLoader(settings),
            CatalogFormat.IMAGE: ImageLoader(settings),
            CatalogFormat.EXCEL: ExcelLoader(settings),
            CatalogFormat.WORD: WordLoader(settings),
            CatalogFormat.POWERPOINT: PptxLoader(settings),
        }

    def load(self, path: Path) -> list[CatalogPage]:
        catalog_format = self._EXTENSIONS.get(path.suffix.lower())
        if catalog_format is None:
            raise UnsupportedFormatError(str(path))

        loader = self._loaders[catalog_format]
        return loader.load(path)
