from qdrant_client import QdrantClient
from utils.embedding_utils import EmbeddingService

COLLECTION_NAME = "documents_chunks"

# Connect to Qdrant
client = QdrantClient(host="localhost", port=6333)

# Initialize embedding service
embedding_service = EmbeddingService()

# User query (semantic search)
query_text = "How does semantic search work in enterprise systems?"

# Convert query to vector
query_vector = embedding_service.embed_texts([query_text])[0]

# Search Qdrant (NEW API)
results = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,
    limit=3
)

print("Top search results:\n")

for idx, hit in enumerate(results.points, start=1):
    print(f"Result {idx}:")
    print("Score:", hit.score)
    print("Text:", hit.payload.get("text"))
    print("-" * 50)
