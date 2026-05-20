from pathlib import Path
from collections.abc import Iterable

from .types import PathLike


def normalize_to_path(path: PathLike) -> Path:
    """
    Преобразует путь к объекту ``pathlib.Path``.

    :param path: Путь до файла/директории.
    :type path: PathLike
    :return: Путь в виде ``pathlib.Path`` объекта.
    :rtype: pathlib.Path
    """
    return Path(path)


def normalize_to_paths(paths: PathLike | Iterable[PathLike]) -> list[Path]:
    """
    Преобразует путь/пути к списку ``pathlib.Path`` объектов.

    :param paths: Путь/пути до файлов/директорий.
    :type paths: PathLike | Iterable[PathLike]
    :return: Список путей в виде ``pathlib.Path`` объектов.
    :rtype: list[pathlib.Path]
    """
    if isinstance(paths, (str, Path)):
        return [normalize_to_path(paths)]
    return [normalize_to_path(p) for p in paths]
