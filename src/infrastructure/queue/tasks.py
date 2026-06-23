import logging
from uuid import UUID

from src.utils import to_path
from src.bootstrap import create_process_handler
from src.domain.enums import PreprocessProfile
from src.application.commands import ProcessCatalogCommand

from .celery_app import celery_app
from .async_runner import run_async

logger = logging.getLogger(__name__)


@celery_app.task(name="catalog.process", bind=True, max_retries=0)
def process_catalog_task(
    self,
    job_id: str,
    source_path: str,
    output_path: str | None,
    profile: str | None,
) -> str:
    command = ProcessCatalogCommand(
        job_id=UUID(job_id),
        source_path=to_path(source_path),
        output_path=to_path(output_path) if output_path else None,
        profile=PreprocessProfile(profile) if profile else None,
    )
    handler = create_process_handler()

    try:
        run_async(handler.handle(command))

    except Exception:
        logger.exception(f"Pipeline failed for job {job_id}")

    return job_id
