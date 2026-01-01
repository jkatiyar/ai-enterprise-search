from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.ingest_service import get_document_by_id
from app.core.edue_query import query_edue
from app.services.query_orchestrator import run_hybrid_query


# --------------------------------------------------
# Router configuration
# --------------------------------------------------

router = APIRouter(
    prefix="/edue",
    tags=["Enterprise Document Understanding"]
)


# --------------------------------------------------
# Request schema
# --------------------------------------------------

class EDUERequest(BaseModel):
    document_id: str
    question: str


# --------------------------------------------------
# EDUE ONLY (deterministic, structure-first)
# --------------------------------------------------

@router.post("/query")
def edue_query_endpoint(req: EDUERequest):
    """
    Runs ONLY the Enterprise Document Understanding Engine (EDUE).
    Deterministic, no LLM, no embeddings.
    """

    document = get_document_by_id(req.document_id)

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return query_edue(document, req.question)


# --------------------------------------------------
# HYBRID: EDUE → RAG (side-by-side)
# --------------------------------------------------

@router.post("/hybrid/query")
def hybrid_query_endpoint(req: EDUERequest):
    """
    Runs EDUE first, then RAG.
    Returns both results side-by-side.
    No arbitration yet.
    """

    document = get_document_by_id(req.document_id)

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return run_hybrid_query(document, req.question)
