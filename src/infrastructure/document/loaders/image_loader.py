from pathlib import Path

from PIL import Image

from src.domain.entities import CatalogPage
from src.domain.exceptions import CatalogLoadError

from .base import BaseLoader


class ImageLoader(BaseLoader):
    """Загрузчик каталога из изображения."""

    def load(self, path: Path) -> list[CatalogPage]:
        """Загружает изображение как одностраничный каталог.

        Parameters
        ----------
        path : Path
            Путь к каталогу.

        Returns
        -------
        list[CatalogPage]
            Страница каталога.

        Raises
        ------
        CatalogLoadError
            Если каталог не найден по указанному пути или
            не удалось корректно сконвертировать изображение.
        """
        if not path.exists():
            raise CatalogLoadError(str(path), "File does not exist")

        try:
            image = Image.open(path).convert("RGB")
        except Exception as exc:
            raise CatalogLoadError(str(path), str(exc)) from exc

        return [
            CatalogPage.from_numpy(
                image,
                page_number=0,
                source_path=path,
            )
        ]
