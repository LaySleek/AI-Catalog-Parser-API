from pathlib import Path

import pymupdf

from app.utils import PathLike, normalize_to_path


class PageRendererService:

    def render_pages(
        self,
        pdf_path: PathLike,
        output_dir: PathLike,
        dpi: int = 300,
    ) -> list[Path]:

        pdf_path = normalize_to_path(pdf_path)
        output_dir = normalize_to_path(output_dir)

        pdf_name = pdf_path.stem

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        document = pymupdf.open(pdf_path)

        zoom = dpi / 72
        matrix = pymupdf.Matrix(zoom, zoom)

        rendered_pages: list[Path] = []
        for page_id, page in enumerate(document):

            pix = page.get_pixmap(
                matrix=matrix,
                alpha=False,
            )
            output_path = output_dir / f"{pdf_name}_page_{page_id}.png"
            pix.save(output_path)

            rendered_pages.append(output_path)

        document.close()
        return rendered_pages
