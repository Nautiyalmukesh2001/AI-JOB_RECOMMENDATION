from typing import Optional

try:
    import pdfplumber
except Exception:  # pragma: no cover
    pdfplumber = None


def extract_text_from_pdf(file) -> str:
    if not pdfplumber:
        return ""
    try:
        with pdfplumber.open(file) as pdf:
            return "".join(page.extract_text() or "" for page in pdf.pages)
    except Exception:
        return ""