import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")
MEDIA_ROOT = os.getenv("MEDIA_ROOT", "./media")
MARKETPLACE = os.getenv("MARKETPLACE", "ebay-sandbox")
os.makedirs(MEDIA_ROOT, exist_ok=True)
