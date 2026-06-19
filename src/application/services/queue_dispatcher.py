import logging

from src.domain.entities import PipelineJob
from src.application.commands import ProcessCatalogCommand
from src.application.ports.output import TaskQueuePort, JobRepositoryPort

logger = logging.getLogger(__name__)


class QueueDispatcher:

    def __init__(
        self,
        task_queue: TaskQueuePort,
        job_repository: JobRepositoryPort,
    ) -> None:
        self._task_queue = task_queue
        self._job_repository = job_repository

    async def enqueue(self, command: ProcessCatalogCommand) -> PipelineJob:
        """Добавляет указанную задачу в брокер сообщений.

        Parameters
        ----------
        command : ProcessCatalogCommand
            Команда на обработку каталога.

        Returns
        -------
        PipelineJob
            Поставленная в очередь задача.

        Raises
        ------
        KeyError
            Если задача с указанным ``command.job_id`` не найдена.
        """
        job = self._job_repository.get(command.job_id)
        if job is None:
            raise KeyError(f"Job {command.job_id} not found")

        task_id = await self._task_queue.enqueue(command)
        job.metadata["celery_task_id"] = task_id
        self._job_repository.save(job)

        logger.info(f"Enqueued catalog job {job.id} as Celery task {task_id}")
        return job
