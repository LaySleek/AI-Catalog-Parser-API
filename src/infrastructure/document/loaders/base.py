from abc import abstractmethod
from pathlib import Path

from src.config.settings import Settings, get_settings
from src.domain.entities import CatalogPage


class BaseLoader:
    """Базовый загрузчик каталога."""

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()

    @abstractmethod
    def load(self, path: Path) -> list[CatalogPage]:
        """Загружает страницы каталога.

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
        CatalogLoadError
            Если не удалось загрузить каталог.
        """
        ...
