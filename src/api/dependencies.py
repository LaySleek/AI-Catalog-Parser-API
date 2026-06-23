from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.bootstrap import build_pipeline, build_job_repository
from src.config.settings import Settings, get_settings
from src.application.handlers import (
    GetJobStatusHandler,
    ProcessCatalogHandler,
    ExportNomenclatureHandler
)
from src.application.services import QueueDispatcher
from src.infrastructure.queue.celery_task_queue import CeleryTaskQueue

from .v1 import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="AI Catalog Parser", lifespan=lifespan)

    job_repository = build_job_repository(settings)
    process_handler = ProcessCatalogHandler(
        pipeline=build_pipeline(settings),
        job_repository=job_repository,
        settings=settings,
    )
    queue_dispatcher = QueueDispatcher(
        task_queue=CeleryTaskQueue(),
        job_repository=job_repository,
    )

    app.state.settings = settings
    app.state.job_repository = job_repository
    app.state.process_handler = process_handler
    app.state.queue_dispatcher = queue_dispatcher
    app.state.export_handler = ExportNomenclatureHandler(job_repository)
    app.state.job_status_handler = GetJobStatusHandler(job_repository)


    app.include_router(api_router, prefix="/v1")
    return app


def get_settings_dep() -> Settings:
    return get_settings()


def get_process_handler(request) -> ProcessCatalogHandler:
    return request.app.state.process_handler


def get_queue_dispatcher(request) -> QueueDispatcher:
    return request.app.state.queue_dispatcher


def get_export_handler(request) -> ExportNomenclatureHandler:
    return request.app.state.export_handler


def get_job_status_handler(request) -> GetJobStatusHandler:
    return request.app.state.job_status_handler
