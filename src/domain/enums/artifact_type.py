from enum import StrEnum


class ArtifactType(StrEnum):
    """Типы артефактов, созданные на этапах пайплайна."""

    RAW_DOCUMENT = "raw_document"
    """Каталог в исходном виде."""

    RENDERED_PAGE = "rendered_page"
    """Страница каталога в виде изображения."""

    EXTRACTION_RESULT = "extraction_result"
    """JSON с результатами парсинга товаров со страницы."""

    TRANSLATION_RESULT = "translation_result"
    """JSON с полями товаров, переведенными на русский."""

    LAYOUT_DETECTION = "layout_detection"
    """Задетектированные элементы карточек товаров (изображение, текст и т.д.)."""

    IMAGE_CROP = "image_crop"
    """Изображение товара, обрезанное из исходной страницы."""

    NOMENCLATURE_EXPORT = "nomenclature_export"
    """Экспорт распаршенных товаров в номеклатуру."""
