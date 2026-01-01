from typing import Dict, List
import re
from difflib import SequenceMatcher


# --------------------------------------------------
# Utility functions
# --------------------------------------------------

def _normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def _question_keywords(question: str) -> List[str]:
    stopwords = {
        "what", "is", "are", "the", "a", "an", "of", "to",
        "explain", "describe", "defined", "definition",
        "in", "this", "document"
    }
    return [
        w for w in _normalize(question).split()
        if w not in stopwords and len(w) > 2
    ]


# --------------------------------------------------
# EDUE core query
# --------------------------------------------------

def query_edue(document: Dict, question: str) -> Dict:
    """
    Enterprise Document Understanding Engine (EDUE)

    Section + paragraph based deterministic answering.
    """

    if "sections" not in document:
        return {
            "engine": "edue",
            "question": question,
            "result": {
                "answer": "Information is not available",
                "confidence": 0.05,
                "pages": [],
            },
        }

    q_norm = _normalize(question)
    q_keywords = _question_keywords(question)

    best_section = None
    best_score = 0.0

    # --------------------------------------------------
    # 1️⃣ Section-level matching
    # --------------------------------------------------

    for section in document.get("sections", []):
        title = section.get("title", "")
        title_norm = _normalize(title)

        # Title similarity
        score = _similarity(q_norm, title_norm)

        # Keyword overlap boost
        overlap = sum(1 for k in q_keywords if k in title_norm)
        score += overlap * 0.15

        if score > best_score:
            best_score = score
            best_section = section

    # --------------------------------------------------
    # 2️⃣ Paragraph-level fallback
    # --------------------------------------------------

    best_paragraph = None
    paragraph_score = 0.0

    if best_score < 0.35:
        for section in document.get("sections", []):
            for para in section.get("paragraphs", []):
                para_norm = _normalize(para)
                score = _similarity(q_norm, para_norm)

                overlap = sum(1 for k in q_keywords if k in para_norm)
                score += overlap * 0.1

                if score > paragraph_score:
                    paragraph_score = score
                    best_paragraph = para
                    best_section = section

        best_score = paragraph_score

    # --------------------------------------------------
    # 3️⃣ No reliable match
    # --------------------------------------------------

    if not best_section or best_score < 0.25:
        return {
            "engine": "edue",
            "question": question,
            "result": {
                "answer": "Information is not available",
                "confidence": 0.05,
                "pages": [],
            },
        }

    # --------------------------------------------------
    # 4️⃣ Build answer
    # --------------------------------------------------

    paragraphs = best_section.get("paragraphs", [])
    pages = best_section.get("pages", [])

    if best_paragraph:
        answer_text = best_paragraph.strip()
    else:
        answer_text = " ".join(p.strip() for p in paragraphs)

    answer_text = re.sub(r"\s+", " ", answer_text).strip()

    # --------------------------------------------------
    # 5️⃣ Confidence calibration
    # --------------------------------------------------

    confidence = min(0.95, round(0.4 + best_score, 2))

    return {
        "engine": "edue",
        "question": question,
        "result": {
            "answer": answer_text,
            "confidence": confidence,
            "pages": sorted(set(pages)),
        },
    }
