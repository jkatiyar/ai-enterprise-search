from fastapi import FastAPI
from routes.upload import router as upload_router
from routes.search import router as search_router

app = FastAPI(
    title="Ingestion Service",
    version="1.0.0",
    description="Handles file ingestion for AI Enterprise Search"
)

# Add upload routes
app.include_router(upload_router, prefix="/upload")

# Add search routes
app.include_router(search_router)
