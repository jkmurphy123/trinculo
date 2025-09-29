from typing import Optional
from sqlmodel import SQLModel, Field

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    isbn13: Optional[str] = None
    title: Optional[str] = None
    authors_json: Optional[str] = None  # JSON array of authors
    publisher: Optional[str] = None
    year: Optional[int] = None
    edition: Optional[str] = None
    page_count: Optional[int] = None
    subjects_json: Optional[str] = None  # JSON array of subjects
    raw_metadata_json: Optional[str] = None  # original API payloads

class Photo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: int = Field(index=True, foreign_key="book.id")
    path: str
    kind: str  # cover|spine|page|isbn|unknown
    exif_json: Optional[str] = None

class Appraisal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: int = Field(index=True, foreign_key="book.id")
    target_price: float
    floor_price: float
    comps_json: Optional[str] = None
    suggested_start_price: Optional[float] = None

class Condition(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: int = Field(index=True, foreign_key="book.id")
    grade: Optional[str] = None  # Acceptable|Good|Very Good|Like New
    defects_json: Optional[str] = None  # JSON array of defects
    notes: Optional[str] = None

class Ad(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: int = Field(index=True, foreign_key="book.id")
    title: Optional[str] = None
    description: Optional[str] = None
    thumb_path: Optional[str] = None

class Listing(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: int = Field(index=True, foreign_key="book.id")
    marketplace: str = "ebay-sandbox"
    status: str = "draft"  # draft|posted|error
    url: Optional[str] = None
    fees_json: Optional[str] = None
    external_id: Optional[str] = None  # marketplace listing id
