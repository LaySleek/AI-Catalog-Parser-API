from typing import Protocol, runtime_checkable
from pathlib import Path

from src.application.commands import ExportNomenclatureCommand


@runtime_checkable
class ExportNomenclatureUseCase(Protocol):
    """Входной порт получения файла номенклатуры по завершённой задаче."""

    async def execute(self, command: ExportNomenclatureCommand) -> Path:
        """Возвращает путь к файлу номенклатуры для завершённой задачи.

        Parameters
        ----------
        command : ExportNomenclatureCommand
            Команда с `job_id` завершённой задачи.

        Returns
        -------
        Path
            Путь к файлу с номенклатурой товаров.

        Raises
        ------
        KeyError
            Если задача с данным `job_id` не найдена.
        ValueError
            Если задача ещё не завершена (статус не `COMPLETED`).
        ExportError
            Если экспорт не удался.
        """
        ...
