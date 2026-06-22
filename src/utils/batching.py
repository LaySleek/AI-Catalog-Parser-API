from typing import TypeVar
from collections.abc import Iterator, Sequence

T = TypeVar("T")


def chunked(items: Sequence[T], batch_size: int) -> Iterator[list[T]]:
    """Разбивает последовательность на батчи фиксированного размера.

    Parameters
    ----------
    items : Sequence[T]
        Элементы для разбиения.
    batch_size : int
        Максимальное число элементов в одном батче.

    Yields
    ------
    list[T]
        Очередной батч элементов.
    """
    for start in range(0, len(items), batch_size):
        yield list(items[start : start + batch_size])
