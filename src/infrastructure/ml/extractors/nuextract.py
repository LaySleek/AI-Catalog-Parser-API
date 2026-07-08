import json
import asyncio

from PIL import Image

from src.utils import ProductData
from src.config.settings import Settings, get_settings
from src.domain.entities import CatalogPage
from src.prompts.registry import PromptRegistry, get_prompt_registry
from src.domain.exceptions import InferenceError, ProductExtractionError
from src.infrastructure.ml.clients import VLLMChatClient


class NuExtractExtractor:
    """Экстрактор карточек товаров через NuExtract3."""

    def __init__(
        self,
        client: VLLMChatClient | None = None,
        prompts: PromptRegistry | None = None,
        settings: Settings | None = None,
    ) -> None:
        self._settings = settings or get_settings()
        self._client = client or VLLMChatClient(self._settings)
        self._prompts = prompts or get_prompt_registry()
        self._extractor = self._settings.extractor
        self._semaphore = asyncio.Semaphore(self._extractor.page_batch_size)

    async def extract(self, pages: list[CatalogPage]) -> list[list[ProductData]]:
        """Извлекает карточки товаров со всех страниц параллельно.

        Parameters
        ----------
        pages : list[CatalogPage]
            Страницы каталога для обработки.

        Returns
        -------
        list[list[ProductData]]
            Список извлечённых карточек товаров для каждой страницы.

        Raises
        ------
        InferenceError
            Если запрос к серверу vLLM завершился ошибкой.
        ProductExtractionError
            Если модель вернула невалидный JSON для какой-либо страницы.
        """
        if not pages:
            return []

        return list(
            await asyncio.gather(*(self._extract_page(page) for page in pages))
        )

    async def _extract_page(self, page: CatalogPage) -> list[ProductData]:

        async with self._semaphore:
            raw = await self._run_vlm(page)

        try:
            parsed = json.loads(raw)

        except json.JSONDecodeError as exc:
            raise ProductExtractionError(
                page_number=page.page_number,
                raw_output=raw,
            ) from exc

        return parsed.get("products") or []

    async def _run_vlm(self, page: CatalogPage) -> list[str]:
        """Запускает визуально-лингвистическую модель для извлечения
        карточек товаров со страниц каталога по заданному шаблону.

        Parameters
        ----------
        page : CatalogPage
            Страница каталога.

        Returns
        -------
        str
            JSON-ответ модели.
        """
        prompt = self._prompts.load_extraction_text("user.jinja2")
        template = self._prompts.load_extraction_template()
        data_url = self._client.image_to_data_url(Image.fromarray(page.image))

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": data_url}
                    },
                ],
            }
        ]

        try:
            return await self._client.complete(
                model=self._settings.extractor.model_id,
                messages=messages,
                max_tokens=self._extractor.max_new_tokens,
                template=template,
                prompt=prompt,
                enable_thinking=self._extractor.enable_thinking,
            )
        except Exception as exc:
            raise InferenceError(
                model=self._settings.extractor.model_id,
                reason=str(exc),
            ) from exc
