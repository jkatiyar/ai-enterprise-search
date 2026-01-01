from typing import Dict
from app.utils.rag_utils import generate_answer_from_context


MAX_CONTEXT_CHARS = 3500


def rag_from_edue_context(
    question: str,
    edue_answer: str,
    pages_text: Dict[int, str]
) -> Dict:
    """
    Run RAG ONLY on EDUE-confirmed context.
    pages_text: {page_number: extracted_text}
    """

    # Build context deterministically
    context_blocks = []

    for page, text in pages_text.items():
        if text.strip():
            context_blocks.append(f"[Page {page}]\n{text.strip()}")

    context = "\n\n".join(context_blocks)[:MAX_CONTEXT_CHARS]

    if not context.strip():
        return {
            "query": question,
            "answer": "Information is not available.",
            "confidence": "low",
            "sources": []
        }

    answer = generate_answer_from_context(
        query=question,
        context=context,
        cautious=False  # EDUE already validated relevance
    )

    return {
        "query": question,
        "answer": answer,
        "confidence": "high",
        "sources": [
            {"page": p} for p in pages_text.keys()
        ]
    }
