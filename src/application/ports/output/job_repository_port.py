from uuid import UUID
from typing import Protocol, runtime_checkable

from src.domain.entities import PipelineJob


@runtime_checkable
class JobRepositoryPort(Protocol):
    """Хранилище статусов задач пайплайна."""

    def save(self, job: PipelineJob) -> None:
        """Сохраняет задачу в хранилище.

        Parameters
        ----------
        job : PipelineJob
            Задача пайплайна.
        """
        ...

    def get(self, job_id: UUID) -> PipelineJob | None:
        """Возвращает задачу пайплайна по ID задачи.

        Parameters
        ----------
        job_id : UUID
            ID задачи

        Returns
        -------
        PipelineJob | None
            Задача пайплайна, созраненная по указанному ID.
            Возвращает ``None``, если задача не найдена.
        """
        ...
