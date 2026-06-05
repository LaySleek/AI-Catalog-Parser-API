from typing import Protocol, runtime_checkable

from src.domain.entities import PipelineJob
from src.application.commands import ProcessCatalogCommand


@runtime_checkable
class ProcessCatalogUseCase(Protocol):
    """Входной порт запуска пайплайна обработки каталога."""

    async def execute(self, command: ProcessCatalogCommand) -> PipelineJob:
        """Принимает команду и запускает пайплайн в фоновом режиме.

        Parameters
        ----------
        command : ProcessCatalogCommand
            Команда с путём к файлу каталога и опциональным профилем предобработки.

        Returns
        -------
        PipelineJob
            Созданная задача со статусом `PENDING`.

        Raises
        ------
        CatalogLoadError
            Если файл по указанному пути недоступен.
        UnsupportedFormatError
            Если формат файла не поддерживается.
        """
        ...
