from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ingest_service import process_file

router = APIRouter(prefix="/upload", tags=["Ingestion"])


@router.post("/")
def upload_document(file: UploadFile = File(...)):
    """
    Upload and ingest a document.
    """

    try:
        # ❌ DO NOT await — this is a sync function
        result = process_file(file)

        return {
            "status": "success",
            "details": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
