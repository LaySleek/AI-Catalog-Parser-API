from uuid import UUID

from pydantic import Field, BaseModel


class ProcessCatalogRequest(BaseModel):
    source_path: str = Field(
        description="Path to catalog file"
    )
    output_path: str | None = Field(
        default=None,
        description="Optional output path for nomenclature xlsx",
    )
    profile: str | None = Field(
        default=None,
        description="Preprocess profile: light, dark, low, dense",
    )


class ProcessCatalogResponse(BaseModel):
    job_id: UUID
    status: str


class JobStatusResponse(BaseModel):
    job_id: UUID
    status: str
    current_stage: str | None = None
    errors: list[str] = Field(default_factory=list)
    artifacts: list[str] = Field(default_factory=list)
