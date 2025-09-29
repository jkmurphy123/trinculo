from typing import Optional
from pathlib import Path
# Optional future: pytesseract / pyzbar

def try_read_isbn_from_image(path: str) -> Optional[str]:
    """Stub: return None or a fake ISBN if filename contains 'isbn'.
    Replace with real barcode/ocr later.
    """
    p = Path(path).name.lower()
    if "isbn" in p:
        return "9780140177398"  # example
    return None
