from typing import Protocol, runtime_checkable
from pathlib import Path

from src.domain.entities import BBox, CatalogPage


@runtime_checkable
class ImageStoragePort(Protocol):
    """Порт обрезки и сохранения изображения товара из страницы каталога."""

    def save_crop(
        self,
        page: CatalogPage,
        bbox: BBox,
        name: str,
    ) -> Path:
        """Обрезает изображение страницы по bbox и сохраняет в отдельный файл.

        Parameters
        ----------
        page : CatalogPage
            Страница каталога, из которой вырезается изображение.
        bbox : BBox
            Bounding box в абсолютных пиксельных координатах.
        name : str
            Базовое имя файла без расширения

        Returns
        -------
        Path
            Абсолютный путь к сохранённому файлу.

        Raises
        ------
        OSError
            Если директория не доступна для записи.
        """
        ...
