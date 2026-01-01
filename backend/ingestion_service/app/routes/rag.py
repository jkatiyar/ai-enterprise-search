from fastapi import APIRouter, Query
from services.search_service import semantic_search_with_context

router = APIRouter(
    prefix="/search",
    tags=["Semantic Search"]
)

@router.post("/rag-preview")
def rag_preview(
    query: str = Query(..., description="User search query"),
    limit: int = Query(5, description="Number of chunks to retrieve")
):
    """
    RAG Preview Endpoint:
    - Performs semantic search
    - Builds context from top chunks
    - Returns query, context, and sources
    """
    return semantic_search_with_context(query=query, limit=limit)
