import json
from functools import lru_cache

from src.config.settings import Settings, get_settings


class PromptRegistry:
    """Реестр промптов."""
    """Загружает промпты и JSON-шаблоны из директории, заданной в настройках."""

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._root = self._settings.prompts_dir

    @property
    def root(self) -> str:
        return str(self._root)

    def load_text(self, group: str, version: str, filename: str) -> str:
        """Возвращает содержимое файла, относящегося к промпту модели.

        Parameters
        ----------
        group : str
            Группа моделей (``extraction``, ``translation``).
        version : str
            Версия промпта.
        filename : str
            Имя загружаемого файла.

        Returns
        -------
        str
            Содержмиое файла.
        """
        path = self._root / group / version / filename
        return path.read_text(encoding="utf-8").strip()

    def load_template(self, group: str, version: str) -> dict:
        """Загружает шаблон ответа модели.

        Parameters
        ----------
        group : str
            Группа моделей (``extraction``, ``translation``).
        version : str
            Версия промпта.

        Returns
        -------
        dict
            Словарь с требуемыми полями в ответе модели.
        """
        path = self._root / group / version / "template.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def load_extraction_text(self, filename: str) -> str:
        """Возвращает содержимое файла из файлов промптов модели
        экстрактора товаров.

        Parameters
        ----------
        filename : str
            Имя загружаемого файла.

        Returns
        -------
        str
            Содержимое файла из версии промпта,
            указанной в настройках приложения.
        """
        version = self._settings.prompts.extraction_version
        return self.load_text("extraction", version, filename)

    def load_extraction_template(self) -> dict:
        """Возвращает шаблон ответов модели экстрактора товаров.

        Returns
        -------
        dict
            Словарь с требуемыми полями в ответе модели из версии промпта,
            указанной в настройках приложения.
        """
        version = self._settings.prompts.extraction_version
        return self.load_template("extraction", version)

    def load_translation_text(self, filename: str) -> str:
        """Возвращает содержимое файла из файлов промптов модели
        переводчика товаров.

        Parameters
        ----------
        filename : str
            Имя загружаемого файла.

        Returns
        -------
        str
            Содержимое файла из версии промпта,
            указанной в настройках приложения.
        """
        version = self._settings.prompts.translation_version
        return self.load_text("translation", version, filename)

    def load_translation_template(self) -> dict:
        """Возвращает шаблон ответов модели переводчика товаров.

        Returns
        -------
        dict
            Словарь с требуемыми полями в ответе модели из версии промпта,
            указанной в настройках приложения.
        """
        version = self._settings.prompts.translation_version
        return self.load_template("translation", version)


@lru_cache
def get_prompt_registry() -> PromptRegistry:
    return PromptRegistry()
