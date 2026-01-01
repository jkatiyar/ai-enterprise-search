from typing import Dict, Any, List

from app.utils.embedding_utils import embed_query
from app.utils.qdrant_utils import search_vectors
from app.utils.rag_utils import generate_answer_from_context


STRONG_SCORE_THRESHOLD = 0.25
WEAK_SCORE_THRESHOLD = 0.05
MAX_CONTEXT_CHARS = 3500


def semantic_search_with_context(query: str, limit: int = 5) -> Dict[str, Any]:
    query_vector = embed_query(query)

    hits = search_vectors(
        query_vector=query_vector,
        limit=limit,
    )

    if not hits:
        return _refusal_response(query)

    strong_hits = [h for h in hits if h.get("score", 0) >= STRONG_SCORE_THRESHOLD]

    if strong_hits:
        selected_hits = strong_hits
        low_confidence = False
    else:
        selected_hits = [h for h in hits if h.get("score", 0) >= WEAK_SCORE_THRESHOLD]
        low_confidence = True

    if not selected_hits:
        return _refusal_response(query)

    context_blocks: List[str] = []
    sources: List[Dict[str, Any]] = []

    for h in selected_hits:
        payload = h.get("payload", {})
        text = payload.get("text", "").strip()

        if not text:
            continue

        context_blocks.append(text[:1000])

        sources.append({
            "source": payload.get("source", "unknown"),
            "page": payload.get("page"),
            "score": round(h.get("score", 0), 4),
        })

    context = "\n\n".join(context_blocks)[:MAX_CONTEXT_CHARS]

    if not context.strip():
        return _refusal_response(query)

    answer = generate_answer_from_context(
        query=query,
        context=context,
        cautious=low_confidence
    )

    return {
        "query": query,
        "answer": answer,
        "confidence": "low" if low_confidence else "high",
        "sources": sources,
    }


def _refusal_response(query: str) -> Dict[str, Any]:
    return {
        "query": query,
        "answer": "The document does not contain this information.",
        "confidence": "low",
        "sources": [],
    }
