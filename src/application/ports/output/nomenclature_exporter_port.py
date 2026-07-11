from typing import Protocol, runtime_checkable
from pathlib import Path

from src.domain.entities import Product


@runtime_checkable
class NomenclatureExporterPort(Protocol):
    """Порт экспорта карточек товаров в ZIP-архив с номенклатурой."""

    def export(
        self,
        products: list[Product],
        output_path: Path,
    ) -> Path:
        """Записывает карточки товаров в ZIP-архив с номенклатурой.

        Архив содержит Excel-файл в корне и директорию ``images/``
        с изображениями товаров.

        Parameters
        ----------
        products : list[Product]
            Список товаров для записи.
        output_path : Path
            Путь к выходному ZIP-архиву.

        Returns
        -------
        Path
            Абсолютный путь к записанному архиву.

        Raises
        ------
        ExportError
            Если шаблон не найден или не удалось записать файл.
        ValueError
            Если список ``products`` пустой.
        """
        ...
