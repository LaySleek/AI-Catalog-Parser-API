from pathlib import Path

from src.domain.enums import CatalogFormat
from src.config.settings import Settings
from src.domain.entities import CatalogPage
from src.domain.exceptions import UnsupportedFormatError

from .loaders import BaseLoader, PDFLoader, PptxLoader, WordLoader, ExcelLoader, ImageLoader


class LoaderFactory:
    """Фабрика загрузчиков каталогов."""

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
        self._loaders: dict[CatalogFormat, BaseLoader] = {
            CatalogFormat.PDF: PDFLoader(settings),
            CatalogFormat.IMAGE: ImageLoader(settings),
            CatalogFormat.EXCEL: ExcelLoader(settings),
            CatalogFormat.WORD: WordLoader(settings),
            CatalogFormat.POWERPOINT: PptxLoader(settings),
        }

    def load(self, path: Path) -> list[CatalogPage]:
        """Выбирает загрузчик каталога по расширению файла и загружает
        страницы каталога.
        
        Parameters
        ----------
        path : Path
            Путь к каталогу.

        Returns
        -------
        list[CatalogPage]
            Список страниц каталога.

        Raises
        ------
        UnsupportedFormatError
            Если расширение каталога не поддерживается системой.
        """
        catalog_format = self._EXTENSIONS.get(path.suffix.lower())
        if catalog_format is None:
            raise UnsupportedFormatError(str(path))

        loader = self._loaders[catalog_format]
        return loader.load(path)
