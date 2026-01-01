# app/utils/edue_rag_bridge.py

def build_edue_context(edue_result: dict) -> str:
    """
    Converts EDUE output into a compact, RAG-safe context block.
    """

    if not edue_result:
        return ""

    result = edue_result.get("result", {})
    answer = result.get("answer", "")
    pages = result.get("pages", [])

    if not answer or answer.strip().lower() == "information is not available":
        return ""

    page_info = ""
    if pages:
        page_info = f"(Source pages: {', '.join(map(str, pages))})"

    context = f"""
DOCUMENT EXTRACT (EDUE):
{answer}
{page_info}
""".strip()

    return context
