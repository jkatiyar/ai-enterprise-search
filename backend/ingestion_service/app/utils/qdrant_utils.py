from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

# -------------------------
# Qdrant configuration
# -------------------------
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "documents"


# -------------------------
# Client factory (IMPORTANT)
# -------------------------
def get_qdrant_client() -> QdrantClient:
    """
    Single place to create Qdrant client.
    Used by app + tests.
    """
    return QdrantClient(
        host=QDRANT_HOST,
        port=QDRANT_PORT,
    )


# -------------------------
# Semantic search
# -------------------------
def search_vectors(
    query_vector: List[float],
    limit: int = 5,
    metadata_filter: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Version-stable Qdrant search.
    Always returns normalized dicts.
    """

    client = get_qdrant_client()

    qdrant_filter = None
    if metadata_filter:
        qdrant_filter = Filter(
            must=[
                FieldCondition(
                    key=k,
                    match=MatchValue(value=v),
                )
                for k, v in metadata_filter.items()
            ]
        )

    # Qdrant 1.8.x compatible API
    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=limit,
        query_filter=qdrant_filter,
        with_payload=True,
    )

    results: List[Dict[str, Any]] = []

    for hit in hits:
        results.append({
            "id": hit.id,
            "score": hit.score,
            "payload": hit.payload or {},
        })

    return results
