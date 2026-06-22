import cv2
import numpy as np
from PIL import Image

from src.domain.enums import PreprocessProfile
from src.domain.entities import CatalogPage


class ImagePreprocessor:
    """Препроцессор изображений перед детекцией."""

    @staticmethod
    def page_to_pil(page: CatalogPage) -> Image.Image:
        """Конвертирует страницу каталога в PIL-изображение.

        Parameters
        ----------
        page : CatalogPage
            Страница каталога.

        Returns
        -------
        Image.Image
            Страница каталога в виде PIL-изображения.
        """
        return Image.fromarray(page.image)

    @staticmethod
    def pil_to_cv2(img: Image.Image) -> np.ndarray:
        """Конвертирует PIL-изображение в numpy-массив.

        Parameters
        ----------
        img : Image.Image
            PIL-изображение.

        Returns
        -------
        np.ndarray
            Изображение в виде numpy-массива.
        """
        return cv2.cvtColor(np.array(img.convert("RGB")), cv2.COLOR_RGB2BGR)

    @staticmethod
    def cv2_to_pil(arr: np.ndarray) -> Image.Image:
        """Конвертирует numpy-массив в PIL-изображение.

        Parameters
        ----------
        arr : np.ndarray
            Изображение в виде numpy-массива.

        Returns
        -------
        Image.Image
            PIL-изображение.
        """
        return Image.fromarray(cv2.cvtColor(arr, cv2.COLOR_BGR2RGB))

    @staticmethod
    def apply_clahe(img_bgr: np.ndarray, clip: float = 2.0, tile: int = 8) -> np.ndarray:
        """Применяет адаптивное выравнивание гистограммы к изображению.

        Parameters
        ----------
        img_bgr : np.ndarray
            Исходное RGB-изображение.
        clip : float, optional
            Порог отсечения гистограммы, by default 2.0
        tile : int, optional
            Размер сетки, by default 8

        Returns
        -------
        np.ndarray
            Изображение с примененным адаптивным выравниванием гистограммы.
        """
        lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
        l_channel, a_channel, b_channel = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=clip, tileGridSize=(tile, tile))
        merged = cv2.merge([clahe.apply(l_channel), a_channel, b_channel])

        return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

    @staticmethod
    def apply_unsharp_mask(
        img_bgr: np.ndarray,
        blur_ksize: int = 0,
        sigma: float = 1.5,
        strength: float = 1.5,
        threshold: int = 5,
    ) -> np.ndarray:
        """Применяет нерезкое маскирование к изображению.

        Parameters
        ----------
        img_bgr : np.ndarray
            Исходное RGB-изображение.
        blur_ksize : int, optional
            Размер ядра размытия, by default 0
        sigma : float, optional
            Радиус размытия, by default 1.5
        strength : float, optional
            Интенсивность усиления контраста, by default 1.5
        threshold : int, optional
            Порог различия яркости соседних пикселей, by default 5

        Returns
        -------
        np.ndarray
            Изображение с примененным нерезким маскированием.
        """
        blurred = cv2.GaussianBlur(img_bgr, (blur_ksize, blur_ksize), sigma)
        diff = cv2.subtract(img_bgr.astype(np.int16), blurred.astype(np.int16))
        mask = (np.abs(diff) > threshold).astype(np.float32)
        sharpened = img_bgr.astype(np.float32) + strength * diff * mask

        return np.clip(sharpened, 0, 255).astype(np.uint8)

    @staticmethod
    def apply_edge_overlay(
        img_bgr: np.ndarray,
        low: int = 30,
        high: int = 100,
        weight: float = 0.25,
    ) -> np.ndarray:
        """Выделение контуров на изображении.

        Parameters
        ----------
        img_bgr : np.ndarray
            Исходное RGB-изображение.
        low : int, optional
            Нижний порог для поиска базовых сегментов контуров, by default 30.
        high : int, optional
            Верхний порог для поиска начала сильных контуров, by default 100.
        weight : float, optional
            Вес наложения границ, by default 0.25

        Returns
        -------
        np.ndarray
            Изображение с выделенными контурами.
        """
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, low, high)
        edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR).astype(np.float32)
        blended = img_bgr.astype(np.float32) * (1 - weight) + edges_bgr * weight
        return np.clip(blended, 0, 255).astype(np.uint8)

    @staticmethod
    def apply_gamma(img_bgr: np.ndarray, gamma: float = 1.3) -> np.ndarray:
        """Выполняет гамма-коррекцию изображения.

        Parameters
        ----------
        img_bgr : np.ndarray
            Исходное RGB-изображение.
        gamma : float, optional
            Коэффициент гаммы, by default 1.3

        Returns
        -------
        np.ndarray
            Изображение с примененной гамма-коррекцией.
        """
        lut = np.array(
            [min(255, int((i / 255.0) ** (1.0 / gamma) * 255)) for i in range(256)],
            dtype=np.uint8,
        )
        return cv2.LUT(img_bgr, lut)

    @staticmethod
    def apply_bilateral(
        img_bgr: np.ndarray,
        d: int = 9,
        sigma_color: float = 75,
        sigma_space: float = 75,
    ) -> np.ndarray:
        """Применяет билатеральный фильтр к изображению.

        Parameters
        ----------
        img_bgr : np.ndarray
            Исходное RGB-изображение.
        d : int, optional
            Диаметр окрестности, by default 9.
        sigma_color : float, optional
            Порог различия цветов пикселей для сглаживания, by default 75.
        sigma_space : float, optional
            Радиус влияния соседних пикселей, by default 75.

        Returns
        -------
        np.ndarray
            Изображение с примененным билатеральным фильтром.
        """
        return cv2.bilateralFilter(img_bgr, d, sigma_color, sigma_space)

    @staticmethod
    def apply_morphological_close(img_bgr: np.ndarray, ksize: int = 3) -> np.ndarray:
        """Применяет морфологическое закрытие к изображению.

        Parameters
        ----------
        img_bgr : np.ndarray
            Исходное RGB-изображение.
        ksize : int, optional
            Размер ядра, by default 3.

        Returns
        -------
        np.ndarray
            Изображение с примененным морфологическим закрытием.
        """
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))
        return cv2.morphologyEx(img_bgr, cv2.MORPH_CLOSE, kernel)

    def auto_detect_profile(self, image: Image.Image) -> PreprocessProfile:
        """Автоматически определяет подходящий профиль предобработки
        страницы перед детекцией изображений по статистике распределения
        пикселей на странице.

        Parameters
        ----------
        image : Image.Image
             Страница каталога в виде PIL-изображения.

        Returns
        -------
        PreprocessProfile
            ВЫбранный профиль предобработки страницы.
        """
        arr = np.array(image.convert("L"), dtype=np.float32)
        mean = arr.mean()
        std = arr.std()
        dark_ratio = (arr < 60).mean()

        if dark_ratio > 0.4:
            return PreprocessProfile.DARK_CATALOG
        if std < 35:
            return PreprocessProfile.LOW_CONTRAST
        if mean > 200 and std < 55:
            return PreprocessProfile.DENSE_GRID
        return PreprocessProfile.LIGHT_CATALOG

    def preprocess_for_detection(
        self,
        image: Image.Image,
        profile: PreprocessProfile | None = None,
    ) -> Image.Image:
        """Предобработка страницы перед детекцией изображений.

        Parameters
        ----------
        image : Image.Image
            Страница каталога в виде PIL-изображения.
        profile : PreprocessProfile | None, optional
            Профиль предобработки страницы перед детекцией, by default None

        Returns
        -------
        Image.Image
            Предобработанная страница.
        """
        if profile is None:
            profile = self.auto_detect_profile(image)

        bgr = self.pil_to_cv2(image)

        if profile == PreprocessProfile.LIGHT_CATALOG:
            bgr = self.apply_clahe(bgr, clip=2.0)
            bgr = self.apply_unsharp_mask(bgr, sigma=1.5, strength=1.4)
            bgr = self.apply_edge_overlay(bgr, low=25, high=80, weight=0.2)
        elif profile == PreprocessProfile.DARK_CATALOG:
            bgr = self.apply_gamma(bgr, gamma=1.4)
            bgr = self.apply_clahe(bgr, clip=3.0)
            bgr = self.apply_unsharp_mask(bgr, sigma=1.0, strength=1.2)
        elif profile == PreprocessProfile.LOW_CONTRAST:
            bgr = self.apply_bilateral(bgr)
            bgr = self.apply_clahe(bgr, clip=4.0, tile=4)
            bgr = self.apply_unsharp_mask(bgr, sigma=2.0, strength=1.8)
            bgr = self.apply_edge_overlay(bgr, low=15, high=60, weight=0.15)
        elif profile == PreprocessProfile.DENSE_GRID:
            bgr = self.apply_bilateral(bgr, sigma_color=50, sigma_space=50)
            bgr = self.apply_clahe(bgr, clip=1.5)
            bgr = self.apply_unsharp_mask(bgr, sigma=0.8, strength=2.0)
            bgr = self.apply_morphological_close(bgr, ksize=2)
            bgr = self.apply_edge_overlay(bgr, low=20, high=70, weight=0.3)

        return self.cv2_to_pil(bgr)
