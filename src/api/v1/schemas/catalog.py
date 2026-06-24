from uuid import UUID

from pydantic import Field, BaseModel


class ProcessCatalogResponse(BaseModel):
    job_id: UUID
    status: str


class JobStatusResponse(BaseModel):
    job_id: UUID
    status: str
    current_stage: str | None = None
    errors: list[str] = Field(default_factory=list)
    artifacts: list[str] = Field(default_factory=list)
