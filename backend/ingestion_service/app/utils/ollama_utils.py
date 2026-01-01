import requests
from typing import Optional

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"


def generate_answer(
    prompt: str,
    temperature: float = 0.2,
    max_tokens: int = 512
) -> Optional[str]:
    """
    Low-level Ollama call (NO safety).
    Do NOT use directly in RAG.
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()

    except requests.exceptions.RequestException as e:
        print(f"[Ollama Error] {e}")
        return None


def generate_answer_from_context(
    query: str,
    context: str,
    cautious: bool = False
) -> str:
    """
    RAG-safe LLM call.
    The model is FORCED to answer ONLY from context.
    """

    system_prompt = """
You are a document-grounded assistant.

Rules:
- Answer ONLY using the provided context.
- If the answer is not present, say:
  "The document does not contain this information."
- Do NOT use external knowledge.
- Do NOT guess.
"""

    if cautious:
        system_prompt += "\n- Be extra conservative. If unsure, refuse."

    final_prompt = f"""
{system_prompt}

Context:
{context}

Question:
{query}

Answer:
"""

    answer = generate_answer(final_prompt)

    if not answer:
        return "The document does not contain this information."

    return answer.strip()
