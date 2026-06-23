from uuid import UUID

from fastapi import Request, APIRouter, HTTPException, status

from src.utils import to_path
from src.domain.enums import PreprocessProfile
from src.api.v1.schemas import (
    JobStatusResponse,
    ProcessCatalogRequest,
    ProcessCatalogResponse
)
from src.domain.exceptions import CatalogParserError
from src.application.commands import ProcessCatalogCommand

router = APIRouter()


@router.post("/process", response_model=ProcessCatalogResponse)
async def process_catalog(
    request: Request,
    payload: ProcessCatalogRequest,
) -> ProcessCatalogResponse:
    handler = request.app.state.process_handler
    queue = request.app.state.queue_dispatcher

    profile = (
        PreprocessProfile(payload.profile)
        if payload.profile is not None
        else None
    )
    command = ProcessCatalogCommand(
        source_path=to_path(payload.source_path),
        output_path=to_path(payload.output_path) if payload.output_path else None,
        profile=profile,
    )

    try:
        job = await handler.execute(command)
        await queue.enqueue(command)

    except CatalogParserError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        ) from exc

    return ProcessCatalogResponse(job_id=job.id, status=job.status.value)


@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(request: Request, job_id: UUID) -> JobStatusResponse:
    handler = request.app.state.job_status_handler

    try:
        job = await handler.get_by_id(job_id)

    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        ) from exc

    return JobStatusResponse(
        job_id=job.id,
        status=job.status.value,
        current_stage=job.current_stage.value if job.current_stage else None,
        errors=job.errors,
        artifacts=[artifact.path.name for artifact in job.artifacts],
    )
