from dataclasses import dataclass

from app.domain.entities.bbox import BBox


@dataclass(slots=True)
class LayoutBlock:
    label: str
    confidence: float
    bbox: BBox
