import io

import fitz
import pytesseract
from PIL import Image


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
            pix = page.get_pixmap(dpi=400)
            img = Image.open(io.BytesIO(pix.tobytes()))
            txt = pytesseract.image_to_string(img)
        full_text += txt + "\n"
    return full_text
