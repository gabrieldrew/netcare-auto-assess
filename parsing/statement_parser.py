import re

ICD10_RE = re.compile(r"\b[A-TV-Z][0-9]{2}\b")
TARIFF_RE = re.compile(r"\b\d{5}\b")
AMOUNT_RE = re.compile(r"R\s?\d[\d ,]*\.\d{2}")

def parse_statement(text: str) -> dict:
    """Very naive field extraction – good enough for a demo."""
    return {
        "icd10": sorted(set(ICD10_RE.findall(text))),
        "tariff_codes": TARIFF_RE.findall(text)[:20],
        "amounts": AMOUNT_RE.findall(text),
        "raw_excerpt": text[:2000]
    }