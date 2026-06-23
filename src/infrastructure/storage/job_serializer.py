import json
from uuid import UUID
from typing import Any
from pathlib import Path
from datetime import UTC, datetime

from src.domain.enums import JobStatus, ArtifactType, PipelineStage
from src.domain.entities import PipelineJob, PipelineArtifact


def _dt_to_str(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat()


def _dt_from_str(value: str | None) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(value)


def job_to_dict(job: PipelineJob) -> dict[str, Any]:
    return {
        "id": str(job.id),
        "status": job.status.value,
        "current_stage": (
            job.current_stage.value if job.current_stage is not None else None
        ),
        "artifacts": [
            {
                "id": str(artifact.id),
                "artifact_type": artifact.artifact_type.value,
                "stage": artifact.stage.value,
                "path": str(artifact.path),
                "metadata": artifact.metadata,
                "created_at": _dt_to_str(artifact.created_at),
            }
            for artifact in job.artifacts
        ],
        "metadata": job.metadata,
        "errors": job.errors,
        "created_at": _dt_to_str(job.created_at),
        "updated_at": _dt_to_str(job.updated_at),
        "started_at": _dt_to_str(job.started_at),
        "finished_at": _dt_to_str(job.finished_at),
        "retry_count": job.retry_count,
    }


def job_from_dict(data: dict[str, Any]) -> PipelineJob:
    artifacts = [
        PipelineArtifact(
            id=UUID(artifact["id"]),
            artifact_type=ArtifactType(artifact["artifact_type"]),
            stage=PipelineStage(artifact["stage"]),
            path=Path(artifact["path"]),
            metadata=artifact.get("metadata") or {},
            created_at=_dt_from_str(artifact["created_at"])
            or datetime.now(UTC),
        )
        for artifact in data.get("artifacts") or []
    ]

    current_stage_raw = data.get("current_stage")
    return PipelineJob(
        id=UUID(data["id"]),
        status=JobStatus(data["status"]),
        current_stage=(
            PipelineStage(current_stage_raw)
            if current_stage_raw is not None
            else None
        ),
        artifacts=artifacts,
        metadata=data.get("metadata") or {},
        errors=list(data.get("errors") or []),
        created_at=_dt_from_str(data["created_at"]) or datetime.now(UTC),
        updated_at=_dt_from_str(data["updated_at"]) or datetime.now(UTC),
        started_at=_dt_from_str(data.get("started_at")),
        finished_at=_dt_from_str(data.get("finished_at")),
        retry_count=int(data.get("retry_count") or 0),
    )


def serialize_job(job: PipelineJob) -> str:
    return json.dumps(job_to_dict(job), ensure_ascii=False)


def deserialize_job(payload: str) -> PipelineJob:
    return job_from_dict(json.loads(payload))
