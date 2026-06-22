import re
import json

import torch
from PIL import Image

from src.utils import ProductData, chunked
from src.config.settings import Settings, get_settings
from src.domain.entities import CatalogPage
from src.prompts.registry import PromptRegistry, get_prompt_registry
from src.domain.exceptions import ProductExtractionError
from src.infrastructure.ml.registry.model_registry import ModelRegistry


class NuExtractExtractor:
    """Экстрактор карточек товаров через NuExtract3."""

    def __init__(
        self,
        registry: ModelRegistry | None = None,
        prompts: PromptRegistry | None = None,
        settings: Settings | None = None,
    ) -> None:
        self._registry = registry or ModelRegistry.get()
        self._prompts = prompts or get_prompt_registry()
        self._settings = settings or get_settings()
        self._extractor = self._settings.extractor

    def extract(self, pages: list[CatalogPage]) -> list[list[ProductData]]:

        if not pages:
            return []

        per_page: list[list[ProductData]] = []

        for page_batch in chunked(pages, self._extractor.page_batch_size):
            images = [Image.fromarray(page.image) for page in page_batch]
            raw_outputs = self._run_vlm(images)

            for page, raw in zip(page_batch, raw_outputs):
                try:
                    parsed = json.loads(raw)

                except json.JSONDecodeError as exc:
                    raise ProductExtractionError(
                        page_number=page.page_number,
                        raw_output=raw,
                    ) from exc

                products = parsed.get("products") or []
                per_page.append(products)

        return per_page

    def _run_vlm(self, images: list[Image.Image]) -> list[str]:
        """Запускает визуально-лингвистическую модель для извлечения
        карточек товаров со страниц каталога по заданному шаблону.

        Parameters
        ----------
        images : list[Image.Image]
            Список изображений страниц каталога.

        Returns
        -------
        list[str]
            Список карточек товаров, найденных на страницах каталога.
        """
        prompt = self._prompts.load_extraction_text("user.jinja2")
        template = self._prompts.load_extraction_template()

        messages = [
            [
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "image": image},
                        {"type": "text", "text": prompt},
                    ],
                }
            ]
            for image in images
        ]

        processor = self._registry.extractor_processor
        model = self._registry.extractor

        inputs = processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
            enable_thinking=self._extractor.enable_thinking,
            template=json.dumps(template, indent=4),
            padding=True,
        ).to(model.device)

        with torch.inference_mode():
            generated_ids = model.generate(
                **inputs,
                max_new_tokens=self._extractor.max_new_tokens,
                do_sample=False,
            )

        generated_ids = generated_ids[:, inputs.input_ids.shape[1]:]
        outputs: list[str] = processor.batch_decode(
            generated_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )

        # Удаление токенов рассуждения из ответа
        if self._extractor.enable_thinking:
            outputs = [
                re.sub(
                    pattern=r'.*?</think>',
                    repl='',
                    string=output,
                    flags=re.DOTALL,
                )
                for output in outputs
            ]

        return [output.strip() for output in outputs]
