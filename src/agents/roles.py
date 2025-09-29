import json
from sqlmodel import Session, select
from ..db.models import Book, Photo, Appraisal, Condition, Ad, Listing
from ..tools_mcp import ocr_server, books_server, imaging_server, db_server, ebay_server

def appraiser_validate(session: Session, book_id: int):
    # Could do checks here; inputs were validated at upload
    return True

def identifier_identify_book(session: Session, book_id: int):
    photos = session.exec(select(Photo).where(Photo.book_id == book_id)).all()
    # Try to read barcode from any photo; else OCR title/author
    isbn = None
    for p in photos:
        isbn = ocr_server.try_read_isbn_from_image(p.path)
        if isbn:
            break

    meta = None
    if isbn:
        meta = books_server.lookup_by_isbn(isbn)
    else:
        # fall back: naive OCR of the best-looking photo
        best = photos[0] if photos else None
        meta = books_server.lookup_by_cover_ocr(best.path) if best else None

    book = session.get(Book, book_id)
    if meta:
        book.isbn13 = meta.get("isbn13")
        book.title = meta.get("title")
        book.authors_json = json.dumps(meta.get("authors", []))
        book.publisher = meta.get("publisher")
        book.year = meta.get("year")
        book.edition = meta.get("edition")
        book.page_count = meta.get("page_count")
        book.subjects_json = json.dumps(meta.get("subjects", []))
        book.raw_metadata_json = json.dumps(meta.get("raw", {}))
        session.add(book)
        session.commit()

def condition_grade_book(session: Session, book_id: int):
    # Super-naive placeholder that assigns 'Good'
    cond = Condition(book_id=book_id, grade="Good", defects_json=json.dumps([]), notes=None)
    session.add(cond)
    session.commit()

def copywriter_create_ad(session: Session, book_id: int):
    book = session.get(Book, book_id)
    title = (book.title or "Used Book").strip()[:80]
    desc_lines = []
    if book.title:
        desc_lines.append(f"{book.title}")
    if book.publisher or book.year:
        desc_lines.append(f"Published by {book.publisher or 'Unknown'}{(' ('+str(book.year)+')') if book.year else ''}.")
    desc_lines.append("Condition: Good. Gently used, no major marks noted.")
    desc = " ".join(desc_lines)

    # Select first photo and make a thumbnail
    photo_path = session.exec(select(Photo.path).where(Photo.book_id == book_id)).first()
    thumb_path = imaging_server.make_thumbnail(photo_path) if photo_path else None

    ad = Ad(book_id=book_id, title=title, description=desc, thumb_path=thumb_path)
    session.add(ad)
    session.commit()

def lister_post_listing(session: Session, book_id: int, marketplace: str):
    # Build a payload and hand to the 'marketplace server' (stub)
    book = session.get(Book, book_id)
    ad = session.exec(select(Ad).where(Ad.book_id == book_id)).first()
    appraisal = session.exec(select(Appraisal).where(Appraisal.book_id == book_id)).first()

    payload = {
        "title": ad.title if ad else (book.title or "Used Book"),
        "description": ad.description if ad else "",
        "price_start": appraisal.floor_price if appraisal else 5.0,
        "marketplace": marketplace,
    }
    listing = ebay_server.create_draft_listing(payload, ad.thumb_path if ad else None)
    row = Listing(book_id=book_id, marketplace=marketplace, status="draft", url=listing["url"], external_id=listing["id"])
    session.add(row)
    session.commit()
    return listing["url"]
