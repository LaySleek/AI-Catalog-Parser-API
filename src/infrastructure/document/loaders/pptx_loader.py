from pathlib import Path

from src.domain.entities import CatalogPage
from src.domain.exceptions import CatalogLoadError

from .base import BaseLoader


class PptxLoader(BaseLoader):
    """Загрузчик PowerPoint-каталога."""

    def load(self, path: Path) -> list[CatalogPage]:
        raise CatalogLoadError(
            str(path),
            "PPTX loader is not implemented yet. "
            "Convert the catalog to PDF first",
        )
