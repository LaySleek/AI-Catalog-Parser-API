from pathlib import Path
from dataclasses import field, dataclass

from .blocks import TextBlock, ImageBlock


@dataclass(slots=True)
class PageData:
    page_number: int

    width: int
    height: int

    rendered_image_path: Path | None = None

    text_blocks: list[TextBlock] = field(default_factory=list)
    image_blocks: list[ImageBlock] = field(default_factory=list)
