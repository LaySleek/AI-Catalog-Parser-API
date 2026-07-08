from .base import CatalogParserError


class InferenceError(CatalogParserError):
    """Сбой при обращении к серверу инференса (vLLM)."""

    def __init__(self, *, model: str, reason: str) -> None:
        """
        Parameters
        ----------
        model : str
            Идентификатор модели, к которой выполнялся запрос.
        reason : str
            Описание причины сбоя.
        """
        self.model = model
        self.reason = reason
        super().__init__(f"Inference request to {model!r} failed: {reason}")
