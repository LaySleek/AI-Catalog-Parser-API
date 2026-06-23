from pathlib import Path

from openpyxl import load_workbook

from src.config.settings import Settings, get_settings
from src.domain.entities import Product
from src.domain.exceptions import ExportError

from .column_map_registry import COLUMN_MAPPING


class ExcelNomenclatureExporter:
    """Экспорт карточек товаров в Excel по шаблону номенклатуры."""

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()

    def export(self, products: list[Product], output_path: Path) -> Path:
        if not products:
            raise ValueError("products list must not be empty")

        template_path = self._settings.resolve_path(
            self._settings.paths.nomenclature_template
        )
        if not template_path.exists():
            raise ExportError(
                str(output_path),
                f"Template not found: {template_path}"
            )

        resolved_output = self._settings.resolve_path(output_path)
        resolved_output.parent.mkdir(parents=True, exist_ok=True)

        workbook = load_workbook(template_path)
        sheet = workbook.active
        row = sheet.max_row + 1

        for product in products:
            self._write_row(sheet, row, self._product_to_row(product))
            row += 1

        workbook.save(resolved_output)
        return resolved_output.resolve()

    @staticmethod
    def _product_to_row(product: Product) -> dict[str, object | None]:
        specs = product.specifications

        def _val(name: str) -> float | None:
            measurement = getattr(specs, name, None)
            return measurement.value if measurement is not None else None

        def _unit(name: str) -> str | None:
            measurement = getattr(specs, name, None)
            return measurement.unit if measurement is not None else None

        def _flag(name: str) -> bool:
            return _val(name) is not None

        return {
            "name": product.name,
            "sku": product.sku,
            "weight_unit": _unit("weight"),
            "weight_flag": _flag("weight"),
            "weight_value": _val("weight"),
            "length_unit": _unit("length"),
            "length_flag": _flag("length"),
            "length_value": _val("length"),
            "description": product.description_text,
            "brand": product.brand,
            "manufacturer": product.manufacturer,
            "image_path": str(product.image_path) if product.image_path else None,
            "volume_unit": _unit("volume"),
            "volume_flag": _flag("volume"),
            "volume_value": _val("volume"),
            "square_unit": _unit("square"),
            "square_flag": _flag("square"),
            "square_value": _val("square"),
            "origin_country": None,
        }

    @staticmethod
    def _write_row(sheet, row: int, row_data: dict[str, object | None]) -> None:
        for col_key, value in row_data.items():
            col = COLUMN_MAPPING.get(col_key)
            if col is not None:
                sheet[f"{col}{row}"] = value
