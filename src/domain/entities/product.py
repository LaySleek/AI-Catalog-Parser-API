from typing import Any
from pathlib import Path
from dataclasses import field, dataclass

from src.utils import to_path
from src.domain.value_objects import Price, ImageCenter, Specifications


@dataclass(slots=True)
class Product:

    name: str
    sku: str
    price: Price

    product_center: ImageCenter
    image_path: Path

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
            raise ValueError("Product price must not be empty")

        if self.product_center is None:
            raise ValueError("Product center must not be empty")

        if self.image_path is None:
            raise ValueError("Image path must not be empty")

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

        price: Price | None = None
        price_data = data.get("price", {})

        if (
            price_data.get("value") is not None
            and price_data.get("currency")
        ):
            price = Price(
                value=float(price_data["value"]),
                currency=str(price_data["currency"]).strip(),
            )

        center: ImageCenter | None = None
        center_data = data.get("product_center", {})

        if (
            center_data.get("x") is not None
            and center_data.get("y") is not None
        ):
            center = ImageCenter(
                x=float(center_data["x"]),
                y=float(center_data["y"]),
            )

        image_path_raw = data.get("image_path")
        image_path = (
            to_path(image_path_raw)
            if image_path_raw is not None
            else None
        )

        if price is None:
            raise ValueError("Invalid product price")

        if center is None:
            raise ValueError("Invalid product center")

        if image_path is None:
            raise ValueError("Invalid image path")

        return cls(
            name=str(data.get("name", "")).strip(),
            sku=str(data.get("sku", "")).strip(),
            price=price,
            product_center=center,
            image_path=image_path,
            specifications=Specifications.from_dict(
                data.get("specifications", {})
            ),
            description=list(data.get("description", [])),
            brand=data.get("brand"),
            manufacturer=data.get("manufacturer"),
            page_number=page_number,
        )

    @property
    def description_text(self) -> str:
        """Описание строки, агрегированное в единую строку с разделителем \\n."""
        return "\n".join(self.description)

    @property
    def has_image(self) -> bool:
        """`True`, если путь к изображению товара уже задан."""
        return self.image_path is not None

    def to_dict(self) -> dict[str, Any]:
        """Сериализация карточки товара в словарь.

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
                "y": self.product_center.y
            },
            "image_path": str(self.image_path),
            "page_number": self.page_number,
        }
