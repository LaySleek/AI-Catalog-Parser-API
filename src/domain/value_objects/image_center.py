from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ImageCenter:
    x: float
    y: float

    def __post_init__(self) -> None:
        for axis, val in (("x", self.x), ("y", self.y)):
            if not (0.0 <= val <= 1.0):
                raise ValueError(
                    f"{self.__class__.__name__}.{axis} must be in [0.0, 1.0], got {val}"
                )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(x={self.x:.4f}, y={self.y:.4f})"

    def to_absolute(self, width: float, height: float) -> tuple[float, float]:
        """Пересчитывает нормализованные координаты в абсолютные значения.

        Parameters
        ----------
        width : float
            Абсолютное значение ширины.
        height : float
            Абсолютное значения высоты.

        Returns
        -------
        tuple[float, float]
            Координаты `(x, y)` в абсолютных значениях.
        """
        return self.x * width, self.y * height
