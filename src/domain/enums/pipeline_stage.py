from enum import StrEnum


class PipelineStage(StrEnum):
    """Стадии пайплайна по парсингу каталога с товарами."""

    LOAD_DOCUMENT = "load_document"
    """Загрузка исходного каталога."""

    EXTRACT_PRODUCTS = "extract_products"
    """Парсинг страницы каталога в JSON."""

    TRANSLATE_PRODUCTS = "translate_products"
    """Перевод требуемых полей JSON на русский."""

    DETECT_LAYOUT = "detect_layout"
    """Детекция элементов карточек товаров (изображение, текст и т.д.)."""

    MATCH_IMAGES = "match_images"
    """Поиск bbox с изображением товара."""

    CROP_IMAGES = "crop_images"
    """Обрезка изображения товара по его bbox из исходной страницы."""

    EXPORT_NOMENCLATURE = "export_nomenclature"
    """Экспорт JSON с карточками товаров в номенклатуру."""
