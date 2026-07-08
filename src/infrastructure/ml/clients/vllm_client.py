import json
import base64
from io import BytesIO
from typing import Any

from PIL import Image
from openai import AsyncOpenAI

from src.config.settings import Settings, get_settings


class VLLMChatClient:
    """Обёртка над OpenAI-совместимым API сервера vLLM."""

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._client = AsyncOpenAI(
            base_url=self._settings.vllm.base_url,
            api_key=self._settings.vllm.api_key,
            timeout=self._settings.vllm.timeout_sec,
            max_retries=self._settings.vllm.max_retries,
        )

    @staticmethod
    def image_to_data_url(image: Image.Image) -> str:
        """Кодирует PIL-изображение в data URL для передачи в chat-сообщении.

        Parameters
        ----------
        image : Image.Image
            Исходное изображение.

        Returns
        -------
        str
            Data URL в формате ``data:image/jpeg;base64,<...>``.
        """
        buffer = BytesIO()
        image.convert("RGB").save(buffer, format="JPEG")
        encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return f"data:image/jpeg;base64,{encoded}"

    async def complete(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        template: dict[str, Any],
        prompt: str,
        enable_thinking: bool = False,
        max_tokens: int | None = None,
        temperature: float = 0.0,
    ) -> str:
        """Выполняет запрос к модели через vLLM.

        Parameters
        ----------
        model : str
            Идентификатор модели, обслуживаемой сервером vLLM.
        messages : list[dict[str, Any]]
            Список сообщений в формате OpenAI Chat Completions API.
        template : dict[str, Any]
            JSON-схема шаблона извлечения/перевода NuExtract3.
        prompt : dict[str, Any]
            Промпт для извлечения/перевода NuExtract3.
        enable_thinking : bool
            Включает режим рассуждения модели.
        max_tokens : int | None
            Максимальное число генерируемых токенов, by default None.
        temperature : float, optional
            Температура сэмплирования, by default 0.0.

        Returns
        -------
        str
            Финальный текст ответа модели.
        """
        response = await self._client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            extra_body={
                "chat_template_kwargs": {
                    "template": json.dumps(template, indent=4),
                    "instructions": prompt,
                    "enable_thinking": enable_thinking,
                },
            },
        )
        content = response.choices[0].message.content or ""
        return content.strip()
