from typing import Dict, Any

def lookup_by_isbn(isbn13: str) -> Dict[str, Any]:
    # Stub response; replace with Open Library / Google Books
    return {
        "isbn13": isbn13,
        "title": "Of Mice and Men",
        "authors": ["John Steinbeck"],
        "publisher": "Penguin",
        "year": 1993,
        "edition": "Reprint",
        "page_count": 112,
        "subjects": ["Fiction", "Classics"],
        "raw": {"source": "stub"}
    }

def lookup_by_cover_ocr(image_path: str) -> Dict[str, Any]:
    # Stub fallback
    return {
        "isbn13": None,
        "title": "Unknown Book (OCR Guess)",
        "authors": [],
        "publisher": None,
        "year": None,
        "edition": None,
        "page_count": None,
        "subjects": [],
        "raw": {"source": "cover-ocr-stub"}
    }
