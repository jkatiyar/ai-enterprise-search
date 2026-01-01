from utils.ollama_utils import generate_answer_from_context


def ask(question: str):
    context = """
Revenue increased by 12% year-over-year.
EBITDA margin improved to 18%.
Net profit stood at INR 240 crore.
"""

    print("\nQ:", question)
    answer = generate_answer_from_context(
        query=question,
        context=context
    )
    print("A:", answer)


# ✅ VALID question
ask("What is the EBITDA margin?")

# ❌ INVALID question
ask("Who is the CEO?")
