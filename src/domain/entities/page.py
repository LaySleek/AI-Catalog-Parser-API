from pathlib import Path
from dataclasses import field, dataclass

import numpy as np

from src.utils import PathLike, to_path


@dataclass(slots=True)
class CatalogPage:
    image: np.ndarray
    page_number: int
    source_path: Path | None = field(default=None)

    def __post_init__(self) -> None:
        if self.page_number < 0:
            raise ValueError(
                f"page_number must be >= 0, got {self.page_number}"
            )
        self._validate_image(self.image)

    def __repr__(self) -> str:
        src = f'"{str(self.source_path)}"' if self.source_path else "None"
        return (
            f"{self.__class__.__name__}("
            f"page_number={self.page_number}, "
            f"size={self.width}x{self.height}, "
            f"source_path={src})"
        )

    @staticmethod
    def _validate_image(image: np.ndarray) -> None:
        if not isinstance(image, np.ndarray):
            raise TypeError(
                f"image must be np.ndarray, got {type(image).__name__}"
            )
        if image.ndim != 3 or image.shape[2] != 3:
            raise ValueError(
                f"image must have shape (H, W, 3), got {image.shape}"
            )
        if image.dtype != np.uint8:
            raise ValueError(
                f"image dtype must be uint8, got {image.dtype}"
            )

    @classmethod
    def from_numpy(
        cls,
        image: np.ndarray,
        page_number: int,
        *,
        source_path: PathLike | None = None,
    ) -> "CatalogPage":
        """Возвращает экземпляр `CatalogPage`, инициализрованный переданным
        изображением.

        Parameters
        ----------
        image : np.ndarray
            Массив изображения.
        page_number : int
            Номер страницы каталога.
        source_path : PathLike | None, optional
            Путь к исходному файлу каталога, by default None

        Returns
        -------
        CatalogPage
            Экземпляр `CatalogPage` с изображением `image`.
        """
        arr = np.asarray(image)

        if arr.ndim == 2:
            arr = np.stack([arr, arr, arr], axis=-1)

        if arr.ndim == 3 and arr.shape[2] == 4:
            arr = arr[..., :3]

        if arr.dtype != np.uint8:
            arr = np.clip(arr, 0, 255).astype(np.uint8)

        return cls(
            image=arr,
            page_number=page_number,
            source_path=to_path(source_path) if source_path is not None else None,
        )

    @property
    def height(self) -> int:
        """Высота изображения в пикселях."""
        return int(self.image.shape[0])

    @property
    def width(self) -> int:
        """Ширина изображения в пикселях."""
        return int(self.image.shape[1])

    @property
    def shape(self) -> tuple[int, int, int]:
        """Размерность изображения в формате `(width, height, 3)`."""
        return self.image.shape

    def crop(self, bbox: tuple[int, int, int, int]) -> np.ndarray:
        """Возвращает обрезанное изображение.

        Parameters
        ----------
        bbox : tuple[int, int, int, int]
            Координаты bbox для обрезки изображения.

        Returns
        -------
        np.ndarray
            Изображение, обрезанное по `bbox`.
        """
        x0, y0, x1, y1 = bbox
        y1_c = max(0, int(y0))
        x1_c = max(0, int(x0))
        y2_c = min(self.height, int(y1))
        x2_c = min(self.width, int(x1))
        return self.image[y1_c:y2_c, x1_c:x2_c]

    def copy(self) -> "CatalogPage":
        """Создает полную копию страницы

        Returns
        -------
        CatalogPage
            Экземпляр `CatalogPage`, содержащие полные копии атрибутов.
        """
        return CatalogPage(
            image=self.image.copy(),
            page_number=self.page_number,
            source_path=self.source_path,
        )

    def set_image(self, image: np.ndarray) -> "CatalogPage":
        """Возвращает новый экземпляр `CatalogPage` с замененным
        массивом изображения.

        Parameters
        ----------
        image : np.ndarray
            Массив изображения для замены.

        Returns
        -------
        CatalogPage
            Новый экземпляр `CatalogPage` с тем же `page_number`
            и `source_path` и измененным изображением `image`.
        """
        self._validate_image(image)
        return CatalogPage(
            image=image,
            page_number=self.page_number,
            source_path=self.source_path,
        )
