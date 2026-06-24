from uuid import UUID
from pathlib import Path

import anyio
from fastapi import UploadFile

from src.config.settings import Settings, get_settings
from src.domain.exceptions import UnsupportedFormatError
from src.infrastructure.document import LoaderFactory


class CatalogStorage:
    """Сохраняет загруженный через API файл каталога на диск.

    Parameters
    ----------
    settings : Settings | None, optional
        Конфигурация приложения.
    """
    SUPPORTED_EXTENSIONS: set[str] = set(LoaderFactory._EXTENSIONS)

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._catalogs_dir = self._settings.resolve_path(
            self._settings.paths.catalogs_dir
        )
        self._catalogs_dir.mkdir(parents=True, exist_ok=True)

    async def save(self, file: UploadFile, job_id: UUID) -> Path:
        """Сохраняет загруженный файл каталога и возвращает путь к нему.

        Parameters
        ----------
        file : UploadFile
            Загруженный файл.
        job_id : UUID
            Идентификатор задачи, используется как имя файла.

        Returns
        -------
        Path
            Абсолютный путь к сохранённому файлу.

        Raises
        ------
        UnsupportedFormatError
            Если расширение файла не входит в ``SUPPORTED_EXTENSIONS``.
        """
        suffix = self._validate_extension(file.filename or "")
        dest = self._catalogs_dir / f"{job_id}{suffix}"

        content = await file.read()
        await anyio.to_thread.run_sync(dest.write_bytes, content)

        return dest.resolve()

    def _validate_extension(self, filename: str) -> str:
        """Проверяет расширение файла и возвращает его в нижнем регистре.

        Parameters
        ----------
        filename : str
            Имя файла из ``UploadFile.filename``.

        Returns
        -------
        str
            Расширение файла.

        Raises
        ------
        UnsupportedFormatError
            Если расширение не поддерживается.
        """
        suffix = Path(filename).suffix.lower()
        if suffix not in self.SUPPORTED_EXTENSIONS:
            raise UnsupportedFormatError(filename)

        return suffix
