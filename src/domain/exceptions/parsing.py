from .base import CatalogParserError


class CatalogParseError(CatalogParserError):
    """Ошибка парсинга содержимого каталога."""

    def __init__(self, message: str, *, page_number: int | None = None) -> None:
        """
        Parameters
        ----------
        message : str
            Описание ошибки.
        page_number : int | None, optional
            Номер страницы, на которой произошла ошибка.
        """
        self.page_number = page_number
        suffix = f" (page {page_number})" if page_number is not None else ""
        super().__init__(f"{message}{suffix}")


class NoProductsFoundError(CatalogParseError):
    """Ни на одной странице каталога не найдено валидных товаров."""

    def __init__(self, source_path: str) -> None:
        """
        Parameters
        ----------
        source_path : str
            Путь к файлу каталога.
        """
        self.source_path = source_path
        super().__init__(f"No valid products found in {source_path!r}")


class ProductExtractionError(CatalogParseError):
    """VLM-модель вернула некорректный JSON."""

    def __init__(self, *, page_number: int, raw_output: str) -> None:
        """
        Parameters
        ----------
        page_number : int
            Номер страницы, на которой произошла ошибка.
        raw_output : str
            Исходный вывод модели.
        """
        self.raw_output = raw_output
        super().__init__(
            "VLM returned invalid JSON",
            page_number=page_number,
        )


class LayoutDetectionError(CatalogParseError):
    """Ошибка детекртора изображений для страницы каталога.

    Parameters
    ----------
    page_number : int
        Номер страницы, на которой произошла ошибка.
    reason : str
        Описание причины сбоя.
    """

    def __init__(self, *, page_number: int, reason: str) -> None:
        self.reason = reason
        super().__init__(
            f"Layout detection failed: {reason}",
            page_number=page_number,
        )
