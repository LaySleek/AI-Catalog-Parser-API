from typing import Any, get_args
from dataclasses import field, fields, dataclass


@dataclass(frozen=True, slots=True)
class Measurement:
    value: float
    unit: str

    def __post_init__(self) -> None:
        if not self.unit or not self.unit.strip():
            raise ValueError("Measurement unit must not be empty")

    def __repr__(self) -> str:
        return f"{self.value} {self.unit}"


@dataclass(frozen=True, slots=True)
class Specifications:
    length: Measurement | None = None
    width: Measurement | None = None
    height: Measurement | None = None
    weight: Measurement | None = None
    volume: Measurement | None = None
    square: Measurement | None = None

    other: tuple[str, ...] = field(default_factory=tuple)

    def __repr__(self) -> str:
        parts = []

        for field_name in self._measurement_fields():
            value = getattr(self, field_name)

            if value is not None:
                parts.append(f"{field_name}={value!r}")

        if self.other:
            parts.append(f"other={list(self.other)!r}")

        return f"{self.__class__.__name__}({', '.join(parts)})"

    @classmethod
    def _measurement_fields(cls) -> tuple[str, ...]:
        result: list[str] = []

        for f in fields(cls):
            annotation = f.type

            args = get_args(annotation)
            if Measurement in args:
                result.append(f.name)

        return tuple(result)

    @property
    def is_empty(self) -> bool:
        """`True`, если ни одна характеристика не задана."""
        standard = (
            self.length, self.width, self.height,
            self.weight, self.volume, self.square,
        )
        return all(m is None for m in standard) and len(self.other) == 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Specifications":
        """Возвращает экземпляр `Specifications`, инициализированный
        значениями из словаря.

        Parameters
        ----------
        data : dict[str, Any]
            Данные о технических характеристиках товара.

        Returns
        -------
        Specifications
            Экземпляр `Specifications` с данными из `data`.
        """
        kwargs: dict[str, Any] = {}

        for field_name in cls._measurement_fields():
            raw = data.get(field_name) or {}
            value = raw.get("value")
            unit = raw.get("unit")

            if value is not None and unit is not None:
                try:
                    kwargs[field_name] = Measurement(
                        value=float(value),
                        unit=str(unit).strip(),
                    )
                except (TypeError, ValueError):
                    kwargs[field_name] = None
            else:
                kwargs[field_name] = None

        raw_other = data.get("other") or []
        kwargs["other"] = tuple(str(s) for s in raw_other if s)

        return cls(**kwargs)

    def to_dict(self) -> dict[str, Any]:
        """Сериализует технические характеристики в словарь.

        Returns
        -------
        dict[str, Any]
            Словарь с данными техничесмких ракатеристик.
        """
        result: dict[str, Any] = {}

        for field_name in self._measurement_fields():
            measurement = getattr(self, field_name)

            result[field_name] = (
                None
                if measurement is None
                else {
                    "value": measurement.value,
                    "unit": measurement.unit,
                }
            )

        result["other"] = list(self.other)
        return result
