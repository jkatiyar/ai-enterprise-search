# app/services/query_orchestrator.py

from app.services.search_service import semantic_search_with_context


def run_hybrid_query(document: dict, question: str) -> dict:
    """
    Hybrid = EDUE first, RAG fallback
    """

    print("\n================ HYBRID QUERY START ================\n")
    print(f"Question: {question}")

    # EDUE already ran before calling this function
    edue_result = document.get("edue_result")

    # 1️⃣ If EDUE confidence is acceptable → return EDUE
    if edue_result and edue_result.get("confidence", 0) >= 0.6:
        print("Using EDUE result")
        return {
            "engine": "edue",
            "question": question,
            "result": edue_result,
        }

    # 2️⃣ Otherwise fallback to RAG
    print("Falling back to RAG")

    rag_answer = semantic_search_with_context(question)

    return {
        "engine": "hybrid",
        "question": question,
        "result": {
            "answer": rag_answer,
            "confidence": 0.4,
            "pages": [],
        },
    }
