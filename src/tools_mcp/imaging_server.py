from typing import Optional
from pathlib import Path
from PIL import Image

def make_thumbnail(path: Optional[str], size=(480, 480)) -> Optional[str]:
    if not path:
        return None
    p = Path(path)
    thumb = p.with_name(p.stem + "_thumb" + p.suffix)
    try:
        im = Image.open(p)
        im.thumbnail(size)
        im.save(thumb)
        return str(thumb)
    except Exception:
        return None
