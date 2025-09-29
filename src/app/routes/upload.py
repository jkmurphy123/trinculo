from fastapi import APIRouter, UploadFile, Form
from typing import List, Optional
from ..storage.fs import save_bytes, ext_from_mime
from ...db.models import Book, Photo, Appraisal
from sqlmodel import SQLModel, create_engine, Session
from ..config import DATABASE_URL
from ..supervisor_entry import run_supervisor_pipeline

router = APIRouter()
engine = create_engine(DATABASE_URL, echo=False)

# Ensure tables exist (simple for starter)
SQLModel.metadata.create_all(engine)

@router.post("/submit")
async def submit(
    files: List[UploadFile],
    target_price: float = Form(...),
    floor_price: float = Form(...),
    notes: Optional[str] = Form("", description="Optional user notes")
):
    if len(files) == 0 or len(files) > 4:
        return {"ok": False, "error": "Please upload between 1 and 4 images."}
    if target_price < floor_price:
        return {"ok": False, "error": "Target price must be >= floor price."}

    # Create a book row + appraisal and store photos
    with Session(engine) as session:
        book = Book()
        session.add(book)
        session.commit()
        session.refresh(book)

        for idx, f in enumerate(files):
            content = await f.read()
            ext = ext_from_mime(f.content_type or "image/jpeg")
            filename = f"book_{book.id}_{idx}{ext}"
            path = save_bytes(filename, content)
            photo = Photo(book_id=book.id, path=path, kind="unknown")
            session.add(photo)

        appraisal = Appraisal(book_id=book.id, target_price=target_price, floor_price=floor_price)
        session.add(appraisal)
        session.commit()

    # Kick off the (synchronous) pipeline for the starter
    result = run_supervisor_pipeline(book_id=book.id)

    return {"ok": True, "book_id": book.id, "result": result}
