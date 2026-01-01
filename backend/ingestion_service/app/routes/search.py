from fastapi import APIRouter, Query
from services.search_service import semantic_search_with_context

router = APIRouter(prefix="/search", tags=["Search"])


@router.post("/rag-preview")
def rag_preview(
    query: str = Query(...),
    limit: int = Query(5)
):
    return semantic_search_with_context(query=query, limit=limit)
