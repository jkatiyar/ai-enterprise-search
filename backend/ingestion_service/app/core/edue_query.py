import re
from typing import Dict, List, Tuple


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

MIN_SENTENCE_TOKENS = 8
MAX_SENTENCES = 3

QUESTION_PREFIXES = (
    "what is",
    "how are",
    "how is",
    "explain",
    "define",
)

NOISE_PATTERNS = [
    r"learning objective",
    r"https?://",
    r"www\.",
]


# ---------------------------------------------------------
# Utility cleaners
# ---------------------------------------------------------

def _repair_pdf_artifacts(text: str) -> str:
    """
    Fix common PDF extraction issues.
    """
    text = re.sub(r"-\s+", "", text)          # fix hyphenation
    text = re.sub(r"\s+", " ", text)          # normalize spaces
    return text.strip()


def _is_noise(sentence: str) -> bool:
    s = sentence.lower().strip()

    if len(s.split()) < MIN_SENTENCE_TOKENS:
        return True

    for p in NOISE_PATTERNS:
        if re.search(p, s):
            return True

    if s.startswith(("what is", "explain", "define")):
        return True

    return False


def _split_sentences(text: str) -> List[str]:
    text = _repair_pdf_artifacts(text)
    return re.split(r"(?<=[.!?])\s+", text)


# ---------------------------------------------------------
# Declarative normalization
# ---------------------------------------------------------

def _normalize_to_declarative(question: str, answer: str) -> str:
    q = question.lower().strip()

    if q.startswith("what is"):
        subject = question[7:].strip().rstrip("?")
        return f"{subject} is {answer}"

    if q.startswith("define"):
        subject = question[6:].strip().rstrip("?")
        return f"{subject} is {answer}"

    if q.startswith("how are") or q.startswith("how is"):
        subject = question.split(" ", 2)[-1].rstrip("?")
        return f"{subject} are connected as follows: {answer}"

    return answer


# ---------------------------------------------------------
# Core EDUE Query Engine
# ---------------------------------------------------------

def query_edue(document: Dict, question: str) -> Dict:
    """
    Enterprise Document Understanding Engine (EDUE)

    - Structure-first
    - Deterministic
    - No embeddings
    - No LLMs
    """

    if not document or "sections" not in document:
        return _empty_response(question)

    candidate_sentences: List[Tuple[str, int]] = []

    question_terms = set(
        re.sub(r"[^\w\s]", "", question.lower()).split()
    )

    # -----------------------------------------------------
    # Section scanning
    # -----------------------------------------------------

    for section in document["sections"]:
        header = section.get("header", "")
        paragraphs = section.get("paragraphs", [])
        page = section.get("page")

        combined_text = " ".join([header] + paragraphs)
        combined_text = _repair_pdf_artifacts(combined_text)

        sentences = _split_sentences(combined_text)

        for s in sentences:
            s_clean = s.strip()

            if _is_noise(s_clean):
                continue

            score = sum(
                1 for t in question_terms
                if t in s_clean.lower()
            )

            if score > 0:
                candidate_sentences.append((s_clean, page))

    # -----------------------------------------------------
    # No signal case
    # -----------------------------------------------------

    if not candidate_sentences:
        return _empty_response(question)

    # -----------------------------------------------------
    # Rank & select
    # -----------------------------------------------------

    candidate_sentences.sort(
        key=lambda x: len(x[0]),
        reverse=True
    )

    selected = candidate_sentences[:MAX_SENTENCES]

    answer_text = " ".join(s for s, _ in selected)
    pages = sorted(
        {p for _, p in selected if p is not None}
    )

    answer_text = _normalize_to_declarative(
        question, answer_text
    )

    confidence = min(
        0.9,
        0.4 + 0.2 * len(selected)
    )

    if not pages:
        confidence = min(confidence, 0.6)

    return {
        "engine": "edue",
        "question": question,
        "result": {
            "answer": answer_text.strip(),
            "confidence": round(confidence, 2),
            "pages": pages,
        },
    }


# ---------------------------------------------------------
# Empty response
# ---------------------------------------------------------

def _empty_response(question: str) -> Dict:
    return {
        "engine": "edue",
        "question": question,
        "result": {
            "answer": "Information is not available.",
            "confidence": 0.05,
            "pages": [],
        },
    }
