from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Price:
    value: float
    currency: str

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError(f"Price value must be >= 0, got {self.value}")
        if not self.currency or not self.currency.strip():
            raise ValueError("Currency must not be empty")

    def __repr__(self) -> str:
        return f"Price(value={self.value}, currency={self.currency!r})"
