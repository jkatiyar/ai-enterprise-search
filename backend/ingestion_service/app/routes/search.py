from fastapi import APIRouter
from services.search_service import semantic_search

router = APIRouter(
    prefix="/search",
    tags=["Semantic Search"]
)

@router.post("/")
def search_endpoint(query: str, limit: int = 5):
    results = semantic_search(query, limit)
    return {
        "query": query,
        "results": results
    }
