from typing import Dict


def calibrate_confidence(
    edue_confidence: float,
    pages: list,
    rag_used: bool
) -> Dict:
    """
    Converts raw confidence into calibrated, explainable confidence.
    """

    page_count = len(set(pages)) if pages else 0

    # Base score starts from EDUE
    score = edue_confidence

    # Page-based reinforcement
    if page_count >= 5:
        score += 0.05
    elif page_count >= 3:
        score += 0.03
    elif page_count == 1:
        score -= 0.05

    # RAG reinforcement (only if EDUE already strong)
    if rag_used and edue_confidence >= 0.7:
        score += 0.02

    # Clamp score
    score = max(0.0, min(score, 1.0))

    # Banding
    if score >= 0.9:
        band = "very_high"
        explanation = "Multiple strong matches across document sections"
    elif score >= 0.75:
        band = "high"
        explanation = "Clear and well-supported answer in document"
    elif score >= 0.5:
        band = "medium"
        explanation = "Answer found but partially supported"
    elif score >= 0.25:
        band = "low"
        explanation = "Weak or fragmented references"
    else:
        band = "very_low"
        explanation = "Information likely not present"

    return {
        "raw_score": round(edue_confidence, 2),
        "calibrated_score": round(score, 2),
        "band": band,
        "page_support": page_count,
        "explanation": explanation
    }
