from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BBox:
    x0: float
    y0: float
    x1: float
    y1: float

    def __post_init__(self) -> None:
        if self.x0 > self.x1:
            raise ValueError(
                f"x0 ({self.x0}) must be <= x1 ({self.x1})"
            )
        if self.y0 > self.y1:
            raise ValueError(
                f"y0 ({self.y0}) must be <= y1 ({self.y1})"
            )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"x0={self.x0:.1f}, y0={self.y0:.1f}, "
            f"x1={self.x1:.1f}, y1={self.y1:.1f}, "
            f"w={self.width:.1f}, h={self.height:.1f})"
        )

    @classmethod
    def from_list(cls, coords: list[float]) -> "BBox":
        """Создаёт `BBox` из списка координат.

        Parameters
        ----------
        coords : list[float]
            Список коодинат в формате `[x0, y0, x1, y1]`.

        Returns
        -------
        BBox
            Экземпляр `BBox`, инициализрованный значениями `coords`.

        Raises
        ------
        ValueError
            Если длина списка не равна 4.
        """
        if len(coords) != 4:
            raise ValueError(
                f"Expected 4 coordinates, got {len(coords)}: {coords}"
            )
        return cls(
            x0=coords[0],
            y0=coords[1],
            x1=coords[2],
            y1=coords[3],
        )

    @property
    def width(self) -> float:
        """Ширина bbox в пикселях."""
        return self.x1 - self.x0

    @property
    def height(self) -> float:
        """Высота bbox в пикселях."""
        return self.y1 - self.y0

    @property
    def area(self) -> float:
        """Площадь bbox в квадратных пикселях."""
        return self.width * self.height

    @property
    def center_x(self) -> float:
        """x-координата центра bbox."""
        return (self.x0 + self.x1) / 2.0

    @property
    def center_y(self) -> float:
        """y-координата центра bbox."""
        return (self.y0 + self.y1) / 2.0

    @property
    def is_empty(self) -> bool:
        """Возвращает `True`, если bbox имеет нулевую площадь."""
        return self.width == 0 or self.height == 0

    def to_tuple(self) -> tuple[float, float, float, float]:
        """Возвращает координаты в виде кортежа.

        Returns
        -------
        tuple[float, float, float, float]
            Кортеж с координатами в формате `(x1, y1, x2, y2)`.
        """
        return (self.x0, self.y0, self.x1, self.y1)

    def intersection(self, other: "BBox") -> "BBox | None":
        """Возвращает пересечение двух bbox.

        Parameters
        ----------
        other : BBox
            bbox для поиска пересечения с ним.

        Returns
        -------
        BBox | None
            `Bbox` пересечения или None, если пересечения нет.
        """
        ix1 = max(self.x0, other.x0)
        iy1 = max(self.y0, other.y0)
        ix2 = min(self.x1, other.x1)
        iy2 = min(self.y1, other.y1)

        if ix1 >= ix2 or iy1 >= iy2:
            return None

        return BBox(
            x0=ix1,
            y0=iy1,
            x1=ix2,
            y1=iy2
        )

    def iou(self, other: "BBox") -> float:
        """Intersection over Union (IoU) двух bbox.

        Parameters
        ----------
        other : BBox
            bbox для расчета IoU с ним.

        Returns
        -------
        float
            Значение IoU между двумя bbox в диапазоне `[0.0, 1.0]`.
        """
        inter = self.intersection(other)
        if inter is None:
            return 0.0

        inter_area = inter.area
        union_area = self.area + other.area - inter_area

        if union_area == 0:
            return 0.0

        return inter_area / union_area

    def scale(self, sx: float, sy: float) -> "BBox":
        """Масштабирует bbox с коэффициентами `sx` (по X) и `sy` (по Y).

        Parameters
        ----------
        sx : float
            Коэффициент для оси X.
        sy : float
            Коэффициент для оси Y.

        Returns
        -------
        BBox
            bbox с масштабированными координатами.
        """
        return BBox(
            x0=self.x0 * sx,
            y0=self.y0 * sy,
            x1=self.x1 * sx,
            y1=self.y1 * sy,
        )

    def pad(self, px: float, py: float) -> "BBox":
        """Расширяет bbox на `px` пикселей с каждой стороны по X
        и на `py` пикселей по Y.

        Parameters
        ----------
        px : float
            Размер паддинга для оси X.
        py : float
            Размер паддинга для оси Y.

        Returns
        -------
        BBox
            bbox с примененным паддингом.
        """
        return BBox(
            x0=max(0.0, self.x0 - px),
            y0=max(0.0, self.y0 - py),
            x1=self.x1 + px,
            y1=self.y1 + py,
        )
