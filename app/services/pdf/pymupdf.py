import pymupdf

from app.utils import PathLike, normalize_to_path
from app.domain.entities.bbox import BBox
from app.domain.entities.page import PageData
from app.domain.entities.blocks import TextBlock, ImageBlock


class PyMuPDFService:

    def extract_pages(
        self,
        pdf_path: PathLike,
        image_output_dir: PathLike,
    ) -> list[PageData]:

        pdf_path = normalize_to_path(pdf_path)
        image_output_dir = normalize_to_path(image_output_dir)

        image_output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        document = pymupdf.open(pdf_path)

        pages: list[PageData] = []
        for page_id, page in enumerate(document):

            page_data = PageData(
                page_number=page_id,
                width=int(page.rect.width),
                height=int(page.rect.height),
            )

            #########################
            # TEXT BLOCKS
            #########################
            text_dict = page.get_text("dict")

            for block in text_dict["blocks"]:

                if block["type"] != 0:
                    continue

                bbox = BBox(
                    x0=block["bbox"][0],
                    y0=block["bbox"][1],
                    x1=block["bbox"][2],
                    y1=block["bbox"][3],
                )

                text = ""
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        text += span["text"] + " "

                text = text.strip()
                if not text:
                    continue

                page_data.text_blocks.append(
                    TextBlock(
                        text=text,
                        bbox=bbox,
                        page_id=page_id,
                    )
                )

            #########################
            # IMAGE BLOCKS
            #########################
            image_list = page.get_images(full=True)

            for image_id, image_info in enumerate(image_list):

                xref = image_info[0]
                image_data = document.extract_image(xref)

                image_bytes = image_data["image"]
                ext = image_data["ext"]

                image_path = (
                    image_output_dir
                    / f"page_{page_id}_img_{image_id}.{ext}"
                )

                with open(image_path, "wb") as f:
                    f.write(image_bytes)

                rects = page.get_image_rects(xref)
                for rect in rects:
                    bbox = BBox(
                        x0=rect.x0,
                        y0=rect.y0,
                        x1=rect.x1,
                        y1=rect.y1,
                    )
                    page_data.image_blocks.append(
                        ImageBlock(
                            image_path=image_path,
                            bbox=bbox,
                            page_id=page_id,
                        )
                    )

            pages.append(page_data)

        document.close()
        return pages
