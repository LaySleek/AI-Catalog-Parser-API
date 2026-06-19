from typing import Protocol, runtime_checkable

from src.application.commands import ProcessCatalogCommand


@runtime_checkable
class TaskQueuePort(Protocol):
    """Очередь фоновых задач обработки каталога."""

    async def enqueue(self, command: ProcessCatalogCommand) -> str:
        """Ставит задачу в очередь .


        Parameters
        ----------
        command : ProcessCatalogCommand
            Команда наа обработку каталога.

        Returns
        -------
        str
            Идентификатор сообщения.
        """
        ...
