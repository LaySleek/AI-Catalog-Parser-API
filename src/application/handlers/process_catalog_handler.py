from src.domain.enums import JobStatus
from src.config.settings import Settings, get_settings
from src.domain.entities import PipelineJob, PipelineContext
from src.application.commands import ProcessCatalogCommand
from src.application.pipeline import Pipeline
from src.application.ports.input import ProcessCatalogUseCase
from src.application.ports.output import JobRepositoryPort


class ProcessCatalogHandler(ProcessCatalogUseCase):
    """Обработчик запуска пайплайна обработки каталога."""

    def __init__(
        self,
        pipeline: Pipeline,
        job_repository: JobRepositoryPort,
        settings: Settings | None = None,
    ) -> None:
        self._pipeline = pipeline
        self._job_repository = job_repository
        self._settings = settings or get_settings()

    async def execute(self, command: ProcessCatalogCommand) -> PipelineJob:

        output_path = command.output_path or (
            self._settings.resolve_path(self._settings.paths.nomenclature_dir)
            / f"{command.job_id}.xlsx"
        )

        job = PipelineJob(
            id=command.job_id,
            metadata={
                "source_path": str(command.source_path),
                "output_path": str(output_path),
                "profile": (
                    command.profile.value
                    if command.profile is not None
                    else None
                ),
            },
        )
        self._job_repository.save(job)
        return job

    async def handle(self, command: ProcessCatalogCommand) -> PipelineJob:
        """Запускает задачу на обработку каталога.

        Parameters
        ----------
        command : ProcessCatalogCommand
            Команда для запуска обработки каталогов.

        Returns
        -------
        PipelineJob
            Задача на обработку каталога.

        Raises
        ------
        KeyError
            Если задача с указанным ``command.job_id`` не найдена.
        """
        job = self._job_repository.get(command.job_id)
        if job is None:
            raise KeyError(f"Job {command.job_id} not found")

        job.status = JobStatus.RUNNING
        self._job_repository.save(job)

        context = PipelineContext(job=job)

        try:
            await self._pipeline.run(context)
        except Exception as exc:
            job.fail(str(exc))
            self._job_repository.save(job)
            raise

        self._job_repository.save(job)
        return job
