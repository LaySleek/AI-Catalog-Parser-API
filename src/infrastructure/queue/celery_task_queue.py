from src.application.commands import ProcessCatalogCommand

from .tasks import process_catalog_task


class CeleryTaskQueue:
    """Адаптер Celery для постановки задач обработки каталога в очередь."""

    async def enqueue(self, command: ProcessCatalogCommand) -> str:
        result = process_catalog_task.delay(
            str(command.job_id),
            str(command.source_path),
            str(command.output_path) if command.output_path else None,
            command.profile.value if command.profile is not None else None,
        )
        return result.id
