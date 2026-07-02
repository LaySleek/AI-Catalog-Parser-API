from celery import Celery

from src.config.settings import get_settings

settings = get_settings()

celery_app = Celery(
    "catalog_parser",
    broker=settings.broker_url,
    backend=settings.result_backend_url,
    include=[
        "src.infrastructure.queue.tasks",
        "src.infrastructure.queue.callbacks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_always_eager=settings.celery.task_always_eager,
    task_eager_propagates=settings.celery.task_always_eager,
    task_routes={
        "catalog.process": {"queue": "catalog"},
    },
    task_default_queue="catalog",
)
