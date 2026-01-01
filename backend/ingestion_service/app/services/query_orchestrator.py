from typing import Dict

from app.core.edue_query import query_edue
from app.services.search_service import semantic_search_with_context

EDUE_CONFIDENCE_THRESHOLD = 0.7


def run_hybrid_query(document, question: str) -> Dict:
    """
    Runs EDUE first, then RAG.
    Returns both results side-by-side with explainability.
    """

    # 1️⃣ Run EDUE
    edue_result = query_edue(document, question)
    edue_confidence = edue_result["result"]["confidence"]

    # 2️⃣ Always run RAG (audit + fallback)
    rag_result = semantic_search_with_context(question)

    # 3️⃣ Decide primary engine (NO arbitration yet)
    primary_engine = (
        "edue" if edue_confidence >= EDUE_CONFIDENCE_THRESHOLD else "rag"
    )

    # 4️⃣ Inline explainability (no external service)
    explanation = {
        "steps": [
            "EDUE executed first using document structure and page locality.",
            f"EDUE confidence evaluated as {edue_confidence}.",
            "RAG executed for semantic validation and comparison.",
            f"Primary engine selected: {primary_engine}."
        ],
        "decision_rule": {
            "edue_threshold": EDUE_CONFIDENCE_THRESHOLD,
            "edue_confidence": edue_confidence
        }
    }

    return {
        "query": question,
        "primary_engine": primary_engine,
        "final_answer": (
            edue_result["result"]["answer"]
            if primary_engine == "edue"
            else rag_result["answer"]
        ),
        "confidence": {
            "raw_score": edue_confidence,
            "band": (
                "high" if edue_confidence >= EDUE_CONFIDENCE_THRESHOLD else "low"
            )
        },
        "pages": edue_result["result"].get("pages", []),
        "edue": edue_result,
        "rag": rag_result,
        "explanation": explanation
    }
