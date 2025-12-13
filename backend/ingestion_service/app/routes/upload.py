from fastapi import APIRouter, UploadFile, File, HTTPException
from services.ingest_service import process_file

router = APIRouter()

@router.post("/")
async def upload_document(file: UploadFile = File(...)):
    try:
        result = await process_file(file)
        return {"status": "success", "details": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
