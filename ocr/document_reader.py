import io
import os

import fitz
import pytesseract
from PIL import Image
from .image_reader import extract_text_from_image


def extract_text_from_pdf(file_obj_or_path):
    """Extracts readable text, OCR'ing pages that are image‑only."""
    if hasattr(file_obj_or_path, "read"):
        # Streamlit upload gives a BytesIO‑like object
        buf = file_obj_or_path.read()
        doc = fitz.open(stream=buf, filetype="pdf")
    else:
        doc = fitz.open(file_obj_or_path)

    full_text = ""
    for page in doc:
        txt = page.get_text()
        if len(txt.strip()) < 30:  # likely scanned
            pix = page.get_pixmap(dpi=600)
            img = Image.open(io.BytesIO(pix.tobytes()))
            txt = pytesseract.image_to_string(img)
        full_text += txt + "\n"
    return full_text


def extract_text(file_obj_or_path):
    """Extract text from a PDF or image by auto-detecting the file type."""
    if hasattr(file_obj_or_path, "read"):
        buf = file_obj_or_path.read()
        if buf[:4] == b"%PDF":
            return extract_text_from_pdf(io.BytesIO(buf))
        return extract_text_from_image(io.BytesIO(buf))

    ext = os.path.splitext(str(file_obj_or_path))[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_obj_or_path)
    return extract_text_from_image(file_obj_or_path)
