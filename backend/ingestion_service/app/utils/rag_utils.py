# app/utils/rag_utils.py

from typing import List
import logging

from app.utils.embedding_utils import embed_query
from app.utils.qdrant_utils import search_vectors
from app.utils.ollama_client import generate_answer

# -------------------------------------------------
# Logger (visible with uvicorn --log-level warning)
# -------------------------------------------------
logger = logging.getLogger("rag")


def run_rag_pipeline(
    question: str,
    top_k: int = 5,
) -> str:
    """
    RAG pipeline compatible with existing generate_answer(prompt).
    Incremental addition only. No breaking changes.
    """

    # -------------------------------------------------
    # 1️⃣ Embed query
    # -------------------------------------------------
    query_vector = embed_query(question)

    # -------------------------------------------------
    # 2️⃣ Vector search
    # -------------------------------------------------
    results = search_vectors(
        query_vector=query_vector,
        limit=top_k,
    )

    if not results:
        logger.warning("RAG: No vector search results")
        return "Information is not available."

    # -------------------------------------------------
    # 3️⃣ Build context chunks
    # -------------------------------------------------
    context_chunks: List[str] = []

    for r in results:
        payload = r.get("payload", {})
        text = payload.get("text")
        if text:
            context_chunks.append(text)

    if not context_chunks:
        logger.warning("RAG: Empty context after payload extraction")
        return "Information is not available."

    context = "\n\n".join(context_chunks)

    # -------------------------------------------------
    # 4️⃣ Build final prompt (STRICT grounding)
    # -------------------------------------------------
    final_prompt = f"""
You are answering strictly using the provided context.
If the answer is not present, say "Information is not available".

CONTEXT:
{context}

QUESTION:
{question}
"""

    # -------------------------------------------------
    # 🔍 DEBUG: PROMPT SIZE (THIS IS WHAT WE NEED)
    # -------------------------------------------------
    logger.warning(f"RAG prompt length = {len(final_prompt)}")

    # -------------------------------------------------
    # 5️⃣ Call existing Ollama client (UNCHANGED)
    # -------------------------------------------------
    return generate_answer(final_prompt)
