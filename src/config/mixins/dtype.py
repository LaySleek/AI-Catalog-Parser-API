import torch
from pydantic import Field, BaseModel, field_validator


class TorchDtypeMixin(BaseModel):

    dtype: str | None = Field(
        default=None,
        alias="DTYPE"
    )

    @field_validator("dtype", mode="before")
    @classmethod
    def parse_dtype(cls, v: object) -> torch.dtype | None:

        if v is None:
            return v

        if isinstance(v, str):
            if v.strip() == "":
                return None

            key = v.strip().removeprefix("torch.")
            candidate = getattr(torch, key, None)

            if isinstance(candidate, torch.dtype):
                return candidate

            raise ValueError(f"Неизвестный dtype: {v!r}.")

        raise TypeError(f"Неподдерживаемый тип для dtype: {type(v)}")
