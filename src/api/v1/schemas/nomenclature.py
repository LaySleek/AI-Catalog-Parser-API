from pydantic import BaseModel


class NomenclatureDownloadResponse(BaseModel):
    filename: str
