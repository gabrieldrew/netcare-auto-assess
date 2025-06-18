import io
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import pytesseract


def extract_text_from_image(file_obj_or_path):
    """Extract text from an image file or file-like object using Tesseract OCR."""
    if hasattr(file_obj_or_path, "read"):
        img = Image.open(io.BytesIO(file_obj_or_path.read()))
    else:
        img = Image.open(file_obj_or_path)

    # Convert to a tesseract-friendly format to avoid format errors
    if img.mode not in ("1", "L", "RGB"):
        img = img.convert("RGB")

    # pytesseract uses the image format to determine how to save the
    # temporary file. Some formats like CMYK JPEG can cause failures, so
    # normalise to PNG which is always supported.
    img.format = "PNG"

    # Basic preprocessing to improve recognition of noisy scans
    img = ImageOps.grayscale(img)
    img = ImageOps.autocontrast(img)
    img = img.filter(ImageFilter.SHARPEN)

    # Use English language and automatic page segmentation for better results
    config = "--oem 3 --psm 6"
    return pytesseract.image_to_string(img, lang="eng", config=config)

