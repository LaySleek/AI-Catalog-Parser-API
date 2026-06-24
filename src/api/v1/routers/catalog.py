from uuid import UUID, uuid4

from fastapi import File, Form, Request, APIRouter, UploadFile, HTTPException, status

from src.domain.enums import PreprocessProfile
from src.api.v1.schemas import JobStatusResponse, ProcessCatalogResponse
from src.domain.exceptions import CatalogParserError, UnsupportedFormatError
from src.application.commands import ProcessCatalogCommand

router = APIRouter()


@router.post(
    "/process",
    response_model=ProcessCatalogResponse,
    summary="Загрузить и поставить каталог в очередь обработки",
)
async def process_catalog(
    request: Request,
    file: UploadFile = File(
        ...,
        description="Файл каталога (.pdf, .xlsx, .xls, .docx, .pptx, .png, .jpg, .jpeg)"
    ),
    profile: str | None = Form(
        default=None,
        description="Профиль предобработки: light, dark, low, dense",
    ),
) -> ProcessCatalogResponse:
    """Принимает файл каталога, сохраняет его в ``data/catalogs/`` и ставит
    задачу парсинга в очередь Celery.

    Возвращает ``job_id``.
    """
    catalog_storage = request.app.state.catalog_storage
    handler = request.app.state.process_handler
    queue = request.app.state.queue_dispatcher

    job_id = uuid4()

    try:
        source_path = await catalog_storage.save(file, job_id)

    except UnsupportedFormatError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    parsed_profile = PreprocessProfile(profile) if profile is not None else None

    command = ProcessCatalogCommand(
        job_id=job_id,
        source_path=source_path,
        profile=parsed_profile,
    )

    try:
        job = await handler.execute(command)
        await queue.enqueue(command)

    except CatalogParserError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
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
