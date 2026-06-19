from pathlib import Path

import pymupdf
from PIL import Image

from src.domain.entities import CatalogPage
from src.domain.exceptions import CatalogLoadError

from .base import BaseLoader


class PDFLoader(BaseLoader):
    """Загрузчик PDF-каталога."""

    def load(self, path: Path) -> list[CatalogPage]:
        """Загружает PDF-каталог как список страниц-изображений.

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
            Если каталог не найден по указанному пути или
            не удалось корректно сконвертировать pdf.
        """
        if not path.exists():
            raise CatalogLoadError(str(path), "File does not exist")

        pages: list[CatalogPage] = []
        dpi = self._settings.pdf.render_dpi
        zoom = dpi / 72
        matrix = pymupdf.Matrix(zoom, zoom)

        try:
            document = pymupdf.open(path)
        except Exception as exc:
            raise CatalogLoadError(str(path), str(exc)) from exc

        try:
            for page_number, page in enumerate(document):
                pixmap = page.get_pixmap(matrix=matrix, alpha=False)
                mode = "RGBA" if pixmap.alpha else "RGB"
                image = Image.frombytes(
                    mode,
                    [pixmap.width, pixmap.height],
                    pixmap.samples,
                )
                pages.append(
                    CatalogPage.from_numpy(
                        image,
                        page_number=page_number,
                        source_path=path,
                    )
                )
        finally:
            document.close()

        return pages
