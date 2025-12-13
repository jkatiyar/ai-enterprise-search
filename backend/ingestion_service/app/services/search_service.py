from utils.embedding_utils import EmbeddingService
from utils.qdrant_utils import get_qdrant_client

COLLECTION_NAME = "documents_chunks"

embedding_service = EmbeddingService()

def semantic_search(query: str, limit: int = 5):
    client = get_qdrant_client()

    # Convert query to embedding
    query_vector = embedding_service.embed_texts([query])[0]

    # Perform vector search
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit
    )

    # Format response
    response = []
    for hit in results.points:
        response.append({
            "score": hit.score,
            "text": hit.payload.get("text")
        })

    return response
