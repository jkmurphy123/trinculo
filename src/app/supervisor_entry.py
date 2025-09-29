from sqlmodel import create_engine, Session, select
from ..db.models import Book, Photo, Appraisal, Condition, Ad, Listing
from .config import DATABASE_URL, MARKETPLACE
from ..agents.roles import (
    appraiser_validate,
    identifier_identify_book,
    condition_grade_book,
    copywriter_create_ad,
    lister_post_listing
)

engine = create_engine(DATABASE_URL, echo=False)

def run_supervisor_pipeline(book_id: int):
    """A synchronous, minimal 'supervisor' that runs the pipeline.
    Replace internals with AutoGen GroupChat in Phase 2.
    """
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if not book:
            return {"error": "book not found"}

        # 1) Appraiser validate (here it's trivial—data was collected in POST)
        appraiser_validate(session, book_id)

        # 2) Identifier: fill in metadata from photos
        identifier_identify_book(session, book_id)

        # 3) Condition grading
        condition_grade_book(session, book_id)

        # 4) Copywriter
        copywriter_create_ad(session, book_id)

        # 5) Lister (creates a local stub listing draft)
        url = lister_post_listing(session, book_id, MARKETPLACE)

        return {"pipeline": "ok", "listing_url": url}
