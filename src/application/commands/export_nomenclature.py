from uuid import UUID
from pathlib import Path
from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class ExportNomenclatureCommand:
    """Команда получения экспортированной номенклатуры по завершённой задаче.

    Attributes
    ----------
    job_id : UUID
        Идентификатор завершённой задачи пайплайна.
    output_path : Path | None, optional
        Путь для сохранения файла номенклатуры.
        Если ``None``, то путь определяется из артефактов задачи, by default None.
    """
    job_id: UUID
    output_path: Path | None = None
