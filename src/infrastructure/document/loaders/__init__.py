from .base import BaseLoader
from .pdf_loader import PDFLoader
from .pptx_loader import PptxLoader
from .word_loader import WordLoader
from .excel_loader import ExcelLoader
from .image_loader import ImageLoader

__all__: list[str] = [
    "BaseLoader",
    "ExcelLoader",
    "ImageLoader",
    "PdfLoader",
    "PptxLoader",
    "WordLoader",
]
