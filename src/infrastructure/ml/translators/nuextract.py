import json
import asyncio

from src.utils import ProductData
from src.config.settings import Settings, get_settings
from src.prompts.registry import PromptRegistry, get_prompt_registry
from src.domain.exceptions import InferenceError
from src.infrastructure.ml.clients import VLLMChatClient


class NuExtractTranslator:
    """Переводчик карточек товаров через NuExtract3."""

    def __init__(
        self,
        client: VLLMChatClient | None = None,
        prompts: PromptRegistry | None = None,
        settings: Settings | None = None,
    ) -> None:
        self._settings = settings or get_settings()
        self._client = client or VLLMChatClient(self._settings)
        self._prompts = prompts or get_prompt_registry()
        self._translator = self._settings.translator
        self._semaphore = asyncio.Semaphore(self._translator.product_batch_size)

    async def translate(self, products: list[ProductData]) -> list[ProductData]:
        """Переводит карточки товаров на русский язык параллельно.

        Parameters
        ----------
        products : list[ProductData]
            Карточки товаров, извлечённые `NuExtractExtractor`.

        Returns
        -------
        list[ProductData]
            Переведённые карточки товаров в исходном порядке.

        Raises
        ------
        InferenceError
            Если запрос к серверу vLLM завершился ошибкой.
        """
        if not products:
            return []

        return list(
            await asyncio.gather(*(self._translate_one(p) for p in products))
        )

    async def _translate_one(self, product: ProductData) -> ProductData:
        async with self._semaphore:
            raw = await self._run_vlm(product)

        parsed = json.loads(raw)
        translated_products = parsed.get("products") or []
        return translated_products[0] if translated_products else parsed

    async def _run_vlm(self, product: ProductData) -> str:
        prompt = self._prompts.load_translation_text("user.jinja2")
        template = self._prompts.load_translation_template()

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(product, ensure_ascii=False, indent=2),
                    },
                ],
            }
        ]

        try:
            return await self._client.complete(
                model=self._translator.model_id,
                messages=messages,
                prompt=prompt,
                max_tokens=self._translator.max_new_tokens,
                template=template,
                enable_thinking=self._translator.enable_thinking,
            )
        except Exception as exc:
            raise InferenceError(
                model=self._translator.model_id,
                reason=str(exc),
            ) from exc
