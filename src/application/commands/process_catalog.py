from uuid import UUID, uuid4
from pathlib import Path
from dataclasses import field, dataclass

from src.utils import PathLike, to_path
from src.domain.enums import PreprocessProfile


@dataclass(slots=True, kw_only=True)
class ProcessCatalogCommand:
    """Команда запуска пайплайна обработки каталога.

    Attributes
    ----------
    source_path : Path
        Путь к файлу каталога.
    profile : PreprocessProfile | None, optional
        Профиль предобработки изображений для детектора.
        Если `None`, то профиль определяется автоматически, by default None.
    job_id : UUID, optional
        Идентификатор задачи, by default uuid4.
    """
    source_path: Path
    profile: PreprocessProfile | None = None
    job_id: UUID = field(default_factory=uuid4)

    @classmethod
    def from_path(
        cls,
        path: PathLike,
        *,
        profile: PreprocessProfile | None = None,
    ) -> "ProcessCatalogCommand":
        """Создаёт команду из строки или объекта пути.

        Parameters
        ----------
        path : PathLike
            Путь к файлу каталога.
        profile : PreprocessProfile | None, optional
            Профиль предобработки, by default None.

        Returns
        -------
        ProcessCatalogCommand
            Инициализированная команда с новым `job_id`.
        """
        return cls(
            source_path=to_path(path),
            profile=profile
        )
