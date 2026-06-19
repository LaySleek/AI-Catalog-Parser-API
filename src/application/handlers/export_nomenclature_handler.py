from pathlib import Path

from src.domain.enums import JobStatus, ArtifactType
from src.domain.exceptions import ExportError
from src.application.commands import ExportNomenclatureCommand
from src.application.ports.input import ExportNomenclatureUseCase
from src.application.ports.output import JobRepositoryPort


class ExportNomenclatureHandler(ExportNomenclatureUseCase):

    def __init__(self, job_repository: JobRepositoryPort) -> None:
        self._job_repository = job_repository

    async def execute(self, command: ExportNomenclatureCommand) -> Path:
        job = self._job_repository.get(command.job_id)
        if job is None:
            raise KeyError(f"Job {command.job_id} not found")

        if job.status != JobStatus.COMPLETED:
            raise ExportError(
                str(command.job_id),
                f"Job is not completed: {job.status.value}",
            )

        if command.output_path is not None:
            return command.output_path

        for artifact in job.artifacts:
            if artifact.artifact_type == ArtifactType.NOMENCLATURE_EXPORT:
                return artifact.path

        metadata_path = job.metadata.get("output_path")
        if metadata_path:
            return Path(metadata_path)

        raise ExportError(
            str(command.job_id),
            "Nomenclature export artifact not found",
        )
