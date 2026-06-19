from typing import Protocol, runtime_checkable
from pathlib import Path

from src.domain.entities import CatalogPage


@runtime_checkable
class CatalogLoaderPort(Protocol):
    """Порт загрузки каталога в страницы изображений."""

    def load(self, path: Path) -> list[CatalogPage]:
        """Загружает файл каталога и возвращает список страниц.

        Каждая страница содержит изображение в формате ``(H, W, 3)`` и номер страницы.

        Parameters
        ----------
        path : Path
            Путь к файлу каталога. Поддерживаемые форматы:
            ``.pdf``, ``.xlsx``, ``.xls``, ``.docx``,
            ``.pptx``, ``.png``, ``.jpg``, ``.jpeg``.

        Returns
        -------
        list[CatalogPage]
            Упорядоченный список страниц.

        Raises
        ------
        CatalogLoadError
            Если файл не существует или повреждён.
        UnsupportedFormatError
            Если расширение файла не поддерживается.
        """
        ...
