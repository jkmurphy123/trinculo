from pathlib import Path
from typing import Tuple
from ..config import MEDIA_ROOT

def save_bytes(filename: str, data: bytes) -> str:
    root = Path(MEDIA_ROOT)
    root.mkdir(parents=True, exist_ok=True)
    path = root / filename
    path.write_bytes(data)
    return str(path)

def ext_from_mime(mime: str) -> str:
    return {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
    }.get(mime, ".bin")
