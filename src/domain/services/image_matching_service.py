import numpy as np
from scipy.spatial import cKDTree

from src.domain.entities import BBox, Product, CatalogPage


class ImageMatchingService:
    """Сопоставляет товары с их bbox на странице каталога."""

    def match(
        self,
        page: CatalogPage,
        products: list[Product],
        bboxes: list[BBox],
    ) -> list[tuple[Product, BBox]]:
        """Сопоставляет каждый товар с наиболее подходящим bbox.

        Parameters
        ----------
        page : CatalogPage
            Страница каталога.
        products : list[Product]
            Список товаров, извлечённых VLM с данной страницы.
        bboxes : list[BBox]
            Список bbox изображений, найденных детектором на странице.

        Returns
        -------
        list[tuple[Product, BBox]]
            Список пар (товар, bbox товара).
        """
        if not products:
            return []

        if not bboxes:
            return self._fallback(page, products)

        return self._match_by_kdtree(page, products, bboxes)

    @staticmethod
    def _fallback(
        page: CatalogPage,
        products: list[Product],
    ) -> list[tuple[Product, BBox]]:
        """Назначает bbox ро размеру всей страницы каждому товару.

        Parameters
        ----------
        page : CatalogPage
            Страница каталога.
        products : list[Product]
            Список товаров без обнаруженных bbox.

        Returns
        -------
        list[tuple[Product, BBox]]
            Список товаров, где каждый товар сопоставлен с одним bbox
            по размеру страницы.
        """
        full_page_bbox = BBox(
            x0=0.0,
            y0=0.0,
            x1=float(page.width),
            y1=float(page.height),
        )
        return [(product, full_page_bbox) for product in products]

    @staticmethod
    def _match_by_kdtree(
        page: CatalogPage,
        products: list[Product],
        bboxes: list[BBox],
    ) -> list[tuple[Product, BBox]]:
        """Сопоставляет товары с bbox через KD-дерево.

        Строит KD-дерево по центрам `bboxes` и для каждого товара
        находит ближайший центр.

        Parameters
        ----------
        page : CatalogPage
            Страница каталога.
        products : list[Product]
            Список товаров с нормализованными центрами изображений.
        bboxes : list[BBox]
            Задетекриованные bbox в абсолютных пикселях.

        Returns
        -------
        list[tuple[Product, BBox]]
            Список пар (товар, bbox товара).
        """
        bbox_centers = np.array(
            [[bbox.center_x, bbox.center_y] for bbox in bboxes],
            dtype=np.float32,
        )

        product_centers = np.array(
            [
                product.product_center.to_absolute(page.width, page.height)
                for product in products
            ],
            dtype=np.float32,
        )

        tree = cKDTree(bbox_centers)
        _, indices = tree.query(product_centers, k=1)

        return [
            (product, bboxes[int(idx)])
            for product, idx in zip(products, indices)
        ]
