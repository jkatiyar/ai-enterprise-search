from typing import Dict


def merge_edue_and_rag(edue: Dict, rag: Dict) -> Dict:
    """
    Merge EDUE and RAG answers into a single enterprise-safe answer.
    EDUE = facts
    RAG = explanation / wording only
    """

    edue_answer = edue["result"]["answer"].strip()
    edue_pages = edue["result"]["pages"]
    edue_confidence = edue["result"]["confidence"]

    rag_answer = rag.get("answer", "").strip() if rag else ""

    # Base answer: EDUE is authoritative
    final_answer_parts = [edue_answer]

    # Add RAG only if it adds value and does not contradict
    if rag_answer and rag_answer.lower() not in edue_answer.lower():
        final_answer_parts.append(
            "\n\nExplanation:\n" + rag_answer
        )

    final_answer = "\n".join(final_answer_parts)

    return {
        "final_answer": final_answer,
        "confidence": edue_confidence,
        "pages": edue_pages,
        "composition": {
            "facts_source": "edue",
            "explanation_source": "rag" if rag_answer else "none"
        }
    }
