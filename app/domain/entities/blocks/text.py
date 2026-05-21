from dataclasses import dataclass

from app.domain.entities.bbox import BBox


@dataclass(slots=True)
class TextBlock:
    text: str
    bbox: BBox
    page_id: int
