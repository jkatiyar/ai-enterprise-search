# app/services/search_service.py

from app.utils.rag_utils import run_rag_pipeline


def semantic_search_with_context(
    query: str,
) -> str:
    """
    Pure RAG-based semantic search.
    """

    print("\n================ RAG QUERY ================\n")
    print(f"Query: {query}")

    answer = run_rag_pipeline(query)

    print("\n--- END RAG QUERY ---\n")

    return answer
