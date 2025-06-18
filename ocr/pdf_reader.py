import io
import pathlib

import fitz
import pytesseract
from PIL import Image, ImageOps


def clean_image(img: Image.Image) -> Image.Image:
    """Light preprocessing to improve OCR results."""
    img = ImageOps.exif_transpose(img)
    return img.convert("RGB")


def extract_text_from_image(file_obj, dpi: int = 600, psm: int = 6) -> str:
    img = Image.open(file_obj)
    img = clean_image(img)
    return pytesseract.image_to_string(
        img, lang="eng", config=f"--oem 3 --psm {psm}"
    )


def extract_text(file_obj_or_path, dpi: int = 600, psm: int = 6) -> str:
    """Extract readable text from PDFs or images."""
    name = getattr(file_obj_or_path, "name", str(file_obj_or_path))
    ext = pathlib.Path(name).suffix.lower()
    if ext == ".pdf":
        if hasattr(file_obj_or_path, "read"):
            buf = file_obj_or_path.read()
            doc = fitz.open(stream=buf, filetype="pdf")
        else:
            doc = fitz.open(file_obj_or_path)

        full_text = ""
        for page in doc:
            txt = page.get_text()
            if len(txt.strip()) < 30:  # likely scanned
                pix = page.get_pixmap(dpi=dpi)
                img = Image.open(io.BytesIO(pix.tobytes()))
                txt = pytesseract.image_to_string(
                    clean_image(img), lang="eng", config=f"--oem 3 --psm {psm}"
                )
            full_text += txt + "\n"
        return full_text
    else:
        return extract_text_from_image(file_obj_or_path, dpi, psm)
