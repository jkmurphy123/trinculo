import json
from pathlib import Path
from typing import Dict, Any, Optional

def create_draft_listing(payload: Dict[str, Any], thumb_path: Optional[str]) -> Dict[str, Any]:
    """Stub: writes a JSON file to ./media/listing_drafts and returns a fake URL/id.
    Replace with real eBay Sell Inventory/Offer API calls later.
    """
    out_dir = Path("./media/listing_drafts")
    out_dir.mkdir(parents=True, exist_ok=True)
    listing_id = f"DRAFT-{abs(hash(json.dumps(payload, sort_keys=True))) % 10**8:08d}"
    out_path = out_dir / f"{listing_id}.json"
    doc = {"id": listing_id, "payload": payload, "thumb_path": thumb_path}
    out_path.write_text(json.dumps(doc, indent=2))
    return {"id": listing_id, "url": f"file://{out_path.resolve()}"}
