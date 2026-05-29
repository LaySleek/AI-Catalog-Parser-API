from .base import CatalogParserError


class ExportError(CatalogParserError):
    """Не удалось экспортировать номенклатуру в файл.

    Parameters
    ----------
    output_path : str
        Путь к файлу, в который производился экспорт.
    reason : str
        Техническое описание причины сбоя.

    Examples
    --------
    >>> raise ExportError("data/nomenclature/out.xlsx", "template not found")
    ExportError: Export to 'data/nomenclature/out.xlsx' failed: template not found
    """

    def __init__(self, output_path: str, reason: str) -> None:
        self.output_path = output_path
        self.reason = reason
        super().__init__(
            f"Export to {output_path!r} failed: {reason}"
        )
