from pathlib import Path
from dataclasses import dataclass

from app.domain.entities.bbox import BBox


@dataclass(slots=True)
class ImageBlock:
    image_path: Path
    bbox: BBox
    page_id: int
