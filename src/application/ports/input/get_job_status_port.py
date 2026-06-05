from uuid import UUID
from typing import Protocol, runtime_checkable

from src.domain.entities import PipelineJob


@runtime_checkable
class GetJobStatusUseCase(Protocol):
    """Входной порт получения текущего состояния задачи пайплайна."""

    async def get_by_id(self, job_id: UUID) -> PipelineJob:
        """Возвращает задачу по её идентификатору.

        Parameters
        ----------
        job_id : UUID
            Уникальный идентификатор задачи пайплайна.

        Returns
        -------
        PipelineJob
           Запрошенная задача.

        Raises
        ------
        KeyError
            Если задача с данным `job_id` не найдена в репозитории.
        """
        ...
