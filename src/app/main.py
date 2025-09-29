from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routes.upload import router as upload_router

app = FastAPI(title="Book Lister (AutoGen Starter)")

# API routes
app.include_router(upload_router, prefix="/api")

# Serve the demo frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
