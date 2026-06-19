from pathlib import Path

from pydantic import Field

from src.config.base import AppBaseSettings


class PromptSettings(AppBaseSettings):
    """Версии и расположение промптов для AI-моделей."""

    prompts_dir: Path | None = Field(
        default=None,
        alias="PROMPTS_DIR"
    )
    extraction_version: str = Field(
        default="v1",
        alias="EXTRACTION_PROMPT_VERSION"
    )
    translation_version: str = Field(
        default="v1",
        alias="TRANSLATION_PROMPT_VERSION"
    )

    def resolve_root(self, project_root: Path) -> Path:
        if self.prompts_dir is None:
            return project_root / "src" / "prompts"

        return (
            project_root / self.prompts_dir
            if not self.prompts_dir.is_absolute()
            else self.prompts_dir
        )
