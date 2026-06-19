from pathlib import Path

from pydantic import Field

from src.config.base import AppBaseSettings


class PathSettings(AppBaseSettings):
    """Пути к данным и артефактам проекта."""

    project_root: Path = Field(
        default_factory=lambda: Path(__file__).resolve().parents[3],
        alias="PROJECT_ROOT",
    )
    output_dir: Path = Field(
        default=Path("data/products"),
        alias="OUTPUT_DIR"
    )
    nomenclature_dir: Path = Field(
        default=Path("data/nomenclature"),
        alias="NOMENCLATURE_DIR",
    )
    nomenclature_template: Path = Field(
        default=Path("data/nomenclature/template.xlsx"),
        alias="NOMENCLATURE_TEMPLATE",
    )

    def resolve(self, path: Path) -> Path:
        if path.is_absolute():
            return path
        return self.project_root / path
