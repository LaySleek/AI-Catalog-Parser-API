from celery.signals import worker_ready

from src.config.settings import get_settings
from src.infrastructure.ml.registry import ModelRegistry

settings = get_settings()


@worker_ready.connect
def startup(sender, **kwargs):
    registry = ModelRegistry.get(settings)
    registry.warmup()
