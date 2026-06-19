from typing import Protocol, runtime_checkable

from src.domain.enums import PreprocessProfile
from src.domain.entities import BBox, CatalogPage


@runtime_checkable
class LayoutDetectorPort(Protocol):
    """Порт детекции bounding box-ов изображений на страницах каталога."""

    def detect(
        self,
        pages: list[CatalogPage],
        *,
        profile: PreprocessProfile | None = None,
    ) -> list[list[BBox]]:
        """Детектирует bbox изображений товаров на страницах каталога.

        Parameters
        ----------
        pages : list[CatalogPage]
            Список страниц каталога.

        Returns
        -------
        list[list[BBox]]
            Список bounding box-ов для каждой страницы каталога.

        Raises
        ------
        LayoutDetectionError
            Если детектор завершился с ошибкой для какой-либо страницы.
        """
        ...
