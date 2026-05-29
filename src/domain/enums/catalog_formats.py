from enum import Enum


class CatalogFormat(Enum):
    """Поддерживаемые форматы входного файла каталога."""

    PDF = "pdf"
    EXCEL = "excel"
    WORD = "word"
    POWERPOINT = "pptx"
    IMAGE = "image"
