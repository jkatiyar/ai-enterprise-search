from utils.embedding_utils import embed_query
from utils.qdrant_utils import search_vectors

query = "financial highlights"

print("Embedding query...")
query_vector = embed_query(query)

print("Searching Qdrant...")
results = search_vectors(query_vector=query_vector, limit=5)

print("\nRAW SEARCH RESULTS:\n")

for i, r in enumerate(results, start=1):
    payload = r.get("payload", {})
    print(f"Result {i}")
    print("Score:", r.get("score"))
    print("Text:", payload.get("text", "")[:300])
    print("Source:", payload.get("source"))
    print("Page:", payload.get("page"))
    print("-" * 60)
