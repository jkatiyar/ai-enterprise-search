from fastapi import FastAPI

from app.routes.upload import router as upload_router
from app.routes.edue_query import router as edue_query_router

app = FastAPI(title="Enterprise Document Understanding Engine")

app.include_router(upload_router)
app.include_router(edue_query_router)

@app.get("/")
def health():
    return {"status": "EDUE service running"}
