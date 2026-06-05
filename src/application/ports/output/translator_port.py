from typing import Protocol, runtime_checkable

from src.utils import ProductData


@runtime_checkable
class TranslatorPort(Protocol):
    """Порт перевода карточек товаров на русский язык."""

    def translate(self, products: list[ProductData]) -> list[ProductData]:
        """Переводит список карточек товаров на русский язык.

        Parameters
        ----------
        products : list[ProductData]
            Список сырых словарей товаров из `ProductExtractorPort`.

        Returns
        -------
        list[ProductData]
            Переведённые словари c идентичной входной структурой,
            но измененными текстовыми полями.

        Raises
        ------
        CatalogParseError
            Если модель вернула невалидный JSON для какого-либо товара.
        """
        ...
