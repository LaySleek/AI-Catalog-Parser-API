from pathlib import Path
from functools import lru_cache
from dataclasses import dataclass

from .blocks import (
    ApiSettings,
    PdfSettings,
    PathSettings,
    VllmSettings,
    RedisSettings,
    CelerySettings,
    PromptSettings,
    DetectorSettings,
    ExtractorSettings,
    TranslatorSettings
)


@dataclass(frozen=True, slots=True)
class Settings:
    extractor: ExtractorSettings
    detector: DetectorSettings
    translator: TranslatorSettings
    vllm: VllmSettings
    pdf: PdfSettings
    paths: PathSettings
    api: ApiSettings
    redis: RedisSettings
    celery: CelerySettings
    prompts: PromptSettings

    @classmethod
    def load(cls) -> "Settings":
        return cls(
            extractor=ExtractorSettings(),
            detector=DetectorSettings(),
            translator=TranslatorSettings(),
            vllm=VllmSettings(),
            pdf=PdfSettings(),
            paths=PathSettings(),
            api=ApiSettings(),
            redis=RedisSettings(),
            celery=CelerySettings(),
            prompts=PromptSettings(),
        )

    def resolve_path(self, path: Path) -> Path:
        return self.paths.resolve(path)

    @property
    def prompts_dir(self) -> Path:
        return self.prompts.resolve_root(self.paths.project_root)

    @property
    def broker_url(self) -> str:
        return self.celery.resolve_broker(self.redis.url)

    @property
    def result_backend_url(self) -> str:
        return self.celery.resolve_result_backend(self.redis.url)


@lru_cache
def get_settings() -> Settings:
    return Settings.load()
