from typing import Any
from pathlib import Path
from dataclasses import field, dataclass

from src.utils import to_path
from src.domain.value_objects import Price, ImageCenter, Specifications


@dataclass(slots=True)
class Product:
    """Карточка товара, извлечённая из страницы каталога.

    Attributes
    ----------
    name : str
        Название товара.
    sku : str
        Артикул товара.
    price : Price
        Цена товара.
    product_center : ImageCenter
        Нормализованные координаты центра фотографии товара в диапазоне `[0, 1]`.
    image_path : Path | None, optional
        Путь к обрезанному изображению товара, by default None.
    specifications : Specifications, optional
        Технические характеристики товара, by default `Specifications()`.
    description : list[str], optional
        Список строк описания товара, by default `[]`.
    brand : str | None, optional
        Бренд товара, by default None.
    manufacturer : str | None, optional
        Производитель товара, by default None.
    page_number : int | None, optional
        Номер страницы каталога, с которой извлечён товар, by default None.
    """
    name: str
    sku: str
    price: Price
    product_center: ImageCenter

    image_path: Path | None = None
    specifications: Specifications = field(default_factory=Specifications)
    description: list[str] = field(default_factory=list)
    brand: str | None = None
    manufacturer: str | None = None
    page_number: int | None = None

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Product name must not be empty")

        if not self.sku.strip():
            raise ValueError("Product SKU must not be empty")

        if self.price is None:
            raise ValueError("Product price must not be None")

        if self.product_center is None:
            raise ValueError("Product center must not be None")

    def __repr__(self) -> str:
        return (
            f"Product("
            f"name={self.name!r}, "
            f"sku={self.sku!r}, "
            f"page={self.page_number}, "
            f"has_image={self.has_image})"
        )

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
        *,
        page_number: int | None = None,
    ) -> "Product":
        """Создаёт экземпляр `Product` из словаря.

        Parameters
        ----------
        data : dict[str, Any]
            Словарь с данными товара.
        page_number : int | None, optional
            Номер страницы каталога. Перекрывает значение `data["page_number"]`,
            если задан явно, by default None.

        Returns
        -------
        Product
            Инициализированный экземпляр `Product`.

        Raises
        ------
        ValueError
            Если отсутствуют обязательные поля `price` или `product_center`.
        """
        price: Price | None = None
        price_data: dict[str, Any] = data.get("price") or {}

        if (
            price_data.get("value") is not None
            and price_data.get("currency")
        ):
            price = Price(
                value=float(price_data["value"]),
                currency=str(price_data["currency"]).strip(),
            )

        center: ImageCenter | None = None
        center_data: dict[str, Any] = data.get("product_center") or {}

        if (
            center_data.get("x") is not None
            and center_data.get("y") is not None
        ):
            center = ImageCenter(
                x=float(center_data["x"]),
                y=float(center_data["y"]),
            )

        image_path_raw = data.get("image_path")
        image_path = to_path(image_path_raw) if image_path_raw is not None else None

        if price is None:
            raise ValueError(
                f"Invalid product price for SKU={data.get('sku')!r}: {price_data!r}"
            )

        if center is None:
            raise ValueError(
                f"Invalid product center for SKU={data.get('sku')!r}: {center_data!r}"
            )

        resolved_page = (
            page_number
            if page_number is not None
            else data.get("page_number")
        )

        return cls(
            name=str(data.get("name", "")).strip(),
            sku=str(data.get("sku", "")).strip(),
            price=price,
            product_center=center,
            image_path=image_path,
            specifications=Specifications.from_dict(
                data.get("specifications") or {}
            ),
            description=list(data.get("description") or []),
            brand=data.get("brand"),
            manufacturer=data.get("manufacturer"),
            page_number=resolved_page,
        )

    @property
    def description_text(self) -> str:
        """Описание товара, агрегированное в единую строку с разделителем `\\n`."""
        return "\n".join(self.description)

    @property
    def has_image(self) -> bool:
        """`True`, если путь к изображению товара уже задан."""
        return self.image_path is not None

    def to_dict(self) -> dict[str, Any]:
        """Сериализует карточку товара в словарь.

        Returns
        -------
        dict[str, Any]
            Словарь с данными товара.
        """
        return {
            "name": self.name,
            "sku": self.sku,
            "brand": self.brand,
            "manufacturer": self.manufacturer,
            "description": self.description,
            "price": {
                "value": self.price.value,
                "currency": self.price.currency,
            },
            "specifications": self.specifications.to_dict(),
            "product_center": {
                "x": self.product_center.x,
                "y": self.product_center.y,
            },
            "image_path": str(self.image_path) if self.image_path is not None else None,
            "page_number": self.page_number,
        }
