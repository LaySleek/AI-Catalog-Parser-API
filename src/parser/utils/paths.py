from pathlib import Path

from .types import PathLike


def to_path(path: PathLike) -> Path:
    return Path(path)
