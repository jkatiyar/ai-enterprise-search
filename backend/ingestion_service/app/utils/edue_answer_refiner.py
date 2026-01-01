# app/utils/edue_answer_refiner.py

import re
from typing import List, Dict, Tuple


STOPWORDS = {
    "the", "is", "are", "and", "or", "of", "to", "in", "for",
    "with", "on", "by", "an", "a", "as", "from", "that"
}


def tokenize(text: str) -> List[str]:
    return [
        t.lower()
        for t in re.findall(r"[a-zA-Z0-9]+", text)
        if t.lower() not in STOPWORDS
    ]


def split_into_sentences(text: str) -> List[str]:
    # Robust sentence splitting for PDFs
    text = re.sub(r"\s+", " ", text)
    return re.split(r"(?<=[.!?])\s+", text)


def score_sentence(
    sentence: str,
    question_tokens: List[str],
    header: str = ""
) -> float:
    sentence_tokens = tokenize(sentence)
    if not sentence_tokens:
        return 0.0

    overlap = len(set(sentence_tokens) & set(question_tokens))
    overlap_score = overlap / max(len(question_tokens), 1)

    phrase_bonus = 0.2 if any(
        q in sentence.lower() for q in question_tokens
    ) else 0.0

    header_bonus = 0.1 if header and any(
        q in header.lower() for q in question_tokens
    ) else 0.0

    length_penalty = 0.1 if len(sentence_tokens) > 40 else 0.0

    return overlap_score + phrase_bonus + header_bonus - length_penalty


def refine_edue_answer(
    question: str,
    sections: List[Dict],
    top_k: int = 3
) -> Tuple[str, float, List[int]]:
    """
    Returns:
    - refined answer (string)
    - calibrated confidence (0–1)
    - contributing pages
    """

    question_tokens = tokenize(question)

    scored_sentences = []

    for sec in sections:
        header = sec.get("header", "")
        page = sec.get("page")

        for para in sec.get("paragraphs", []):
            sentences = split_into_sentences(para)
            for s in sentences:
                score = score_sentence(s, question_tokens, header)
                if score > 0:
                    scored_sentences.append({
                        "sentence": s.strip(),
                        "score": score,
                        "page": page
                    })

    if not scored_sentences:
        return "Information is not available.", 0.05, []

    scored_sentences.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    top_sentences = scored_sentences[:top_k]

    answer = " ".join(s["sentence"] for s in top_sentences)
    pages = sorted(set(s["page"] for s in top_sentences if s["page"]))

    # Confidence calibration
    avg_score = sum(s["score"] for s in top_sentences) / len(top_sentences)
    confidence = min(0.95, max(0.3, avg_score))

    return answer, confidence, pages
