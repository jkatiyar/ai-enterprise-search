from typing import Optional

from app.utils.ollama_utils import generate_answer


def generate_answer_from_context(
    query: str,
    context: str,
    cautious: bool = False,
) -> str:
    """
    Generates an answer strictly grounded in provided context.
    Compatible with current Ollama client (no system_prompt support).
    """

    if cautious:
        instruction = (
            "Answer carefully using ONLY the provided context. "
            "If the information is not present, say 'Information is not available.'"
        )
    else:
        instruction = (
            "Answer using ONLY the provided context. "
            "Do not add external knowledge."
        )

    prompt = f"""
{instruction}

Question:
{query}

Context:
{context}

Answer:
""".strip()

    # IMPORTANT:
    # ollama_utils.generate_answer() ONLY accepts 'prompt'
    return generate_answer(prompt)
