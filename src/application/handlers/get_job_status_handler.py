from uuid import UUID

from src.domain.entities import PipelineJob
from src.application.ports.input import GetJobStatusUseCase
from src.application.ports.output import JobRepositoryPort


class GetJobStatusHandler(GetJobStatusUseCase):

    def __init__(self, job_repository: JobRepositoryPort) -> None:
        self._job_repository = job_repository

    async def get_by_id(self, job_id: UUID) -> PipelineJob:
        job = self._job_repository.get(job_id)
        if job is None:
            raise KeyError(f"Job {job_id} not found")
        return job
