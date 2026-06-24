from pathlib import Path

import cv2

from src.config.settings import Settings, get_settings
from src.domain.entities import BBox, CatalogPage


class LocalImageStorage:

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._output_dir = self._settings.resolve_path(self._settings.paths.output_dir)
        self._output_dir.mkdir(parents=True, exist_ok=True)

    def save_crop(
        self,
        page: CatalogPage,
        bbox: BBox,
        name: str,
    ) -> Path:
        filename = f"{self._normalize_name(name)}.png"
        output_path = self._output_dir / filename

        cropped = page.crop(bbox.to_tuple())
        cropped_bgr = cv2.cvtColor(cropped, cv2.COLOR_RGB2BGR)
        cv2.imwrite(str(output_path), cropped_bgr)

        return output_path.resolve()

    @staticmethod
    def _normalize_name(name: str | int) -> str:
        return (
            str(name)
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
            .replace("-", "_")
        )
