from typing import Protocol, runtime_checkable

from src.utils import ProductData
from src.domain.entities import CatalogPage


@runtime_checkable
class ProductExtractorPort(Protocol):
    """Порт извлечения карточек товаров из страниц каталога."""

    async def extract(self, pages: list[CatalogPage]) -> list[list[ProductData]]:
        """Извлекает карточки товаров из батча страниц каталога.

        Parameters
        ----------
        pages : list[CatalogPage]
            Страницы каталога для обработки.

        Returns
        -------
        list[list[ProductData]]
            Список извлеченных данных о каждой карточке товара
            для каждой страницы каталога.

        Raises
        ------
        ProductExtractionError
            Если VLM вернула невалидный JSON для какой-либо страницы.
        """
        ...
