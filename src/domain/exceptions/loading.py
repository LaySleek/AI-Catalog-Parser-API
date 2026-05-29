from pathlib import Path

from .base import CatalogParserError


class CatalogLoadError(CatalogParserError):
    """Ошибка загрузки файла каталога."""

    def __init__(self, path: str, reason: str) -> None:
        """
        Parameters
        ----------
        path : str
            Путь к файлу, при загрузке которого произошла ошибка.
        reason : str
            Описание ошибки.
        """
        self.path = path
        self.reason = reason
        super().__init__(f"Cannot load catalog {path!r}: {reason}")


class UnsupportedFormatError(CatalogLoadError):
    """Ошибка загрузки каталога с не поддерживаемым расширением."""

    def __init__(self, path: str) -> None:
        """
        Parameters
        ----------
        path : str
            Путь к файлу с неизвестным расширением.
        """
        suffix = Path(path).suffix or "<no extension>"
        super().__init__(path, f"unsupported format {suffix!r}")
