import re
import json

import torch

from src.utils import ProductData, chunked
from src.config.settings import Settings, get_settings
from src.prompts.registry import PromptRegistry, get_prompt_registry
from src.infrastructure.ml.registry import ModelRegistry


class NuExtractTranslator:
    """Переводчик карточек товаров через NuExtract3."""

    def __init__(
        self,
        registry: ModelRegistry | None = None,
        prompts: PromptRegistry | None = None,
        settings: Settings | None = None,
    ) -> None:
        self._registry = registry or ModelRegistry.get()
        self._prompts = prompts or get_prompt_registry()
        self._settings = settings or get_settings()
        self._translator = self._settings.translator

    def translate(self, products: list[ProductData]) -> list[ProductData]:
        if not products:
            return []

        translated: list[ProductData] = []

        for product_batch in chunked(products, self._translator.product_batch_size):
            raw_outputs = self._run_translator(product_batch)

            for raw in raw_outputs:
                parsed = json.loads(raw)
                page_products = parsed.get("products") or []
                translated.append(page_products[0] if page_products else parsed)

        return translated

    def _run_translator(self, products: list[ProductData]) -> list[str]:
        """Запускает визуально-лингвистическую модель для перевода информации с
        карточек товаров на русский язык по заданному шаблону.

        Parameters
        ----------
        products : list[ProductData]
            Список карточек товаров.

        Returns
        -------
        list[str]
            Список переведенных карточек товаров.
        """
        prompt = self._prompts.load_translation_text("user.jinja2")
        template = self._prompts.load_translation_template()

        messages = [
            [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "text",
                            "text": json.dumps(product, ensure_ascii=False, indent=2),
                        },
                    ],
                }
            ]
            for product in products
        ]

        processor = self._registry.translator_processor
        model = self._registry.translator

        inputs = processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
            enable_thinking=self._translator.enable_thinking,
            template=json.dumps(template, indent=4),
            padding=True,
        ).to(model.device)

        with torch.inference_mode():
            generated_ids = model.generate(
                **inputs,
                max_new_tokens=self._translator.max_new_tokens,
                do_sample=False,
            )

        generated_ids = generated_ids[:, inputs.input_ids.shape[1]:]
        outputs = processor.batch_decode(
            generated_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )

        # Удаление токенов рассуждения из ответа
        if self._translator.enable_thinking:
            outputs = [
                re.sub(
                    r".*?</think>",
                    "",
                    output,
                    flags=re.DOTALL,
                )
                for output in outputs
            ]

        return [output.strip() for output in outputs]
