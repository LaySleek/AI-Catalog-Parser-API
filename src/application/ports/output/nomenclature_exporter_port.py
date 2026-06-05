from typing import Protocol, runtime_checkable
from pathlib import Path

from src.domain.entities import Product


@runtime_checkable
class NomenclatureExporterPort(Protocol):
    """Порт экспорта карточек товаров в Excel-файл номенклатуры."""

    def export(
        self,
        products: list[Product],
        output_path: Path,
    ) -> Path:
        """Записывает карточки товаров в Excel-файл номенклатуры.

        Parameters
        ----------
        products : list[Product]
            Список товаров для записи.
        output_path : Path
            Путь к выходному файлу номенклатуры.

        Returns
        -------
        Path
            Абсолютный путь к записанному файлу.

        Raises
        ------
        ExportError
            Если шаблон не найден или не удалось записать файл.
        ValueError
            Если список ``products`` пустой.
        """
        ...
