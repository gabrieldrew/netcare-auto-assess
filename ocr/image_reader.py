import io
from PIL import Image
import pytesseract


def extract_text_from_image(file_obj_or_path):
    """Extract text from an image file or file-like object using Tesseract OCR."""
    if hasattr(file_obj_or_path, "read"):
        img = Image.open(io.BytesIO(file_obj_or_path.read()))
    else:
        img = Image.open(file_obj_or_path)
    return pytesseract.image_to_string(img)
