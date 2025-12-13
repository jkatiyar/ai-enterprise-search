from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from utils.embedding_utils import EmbeddingService

# Qdrant connection
client = QdrantClient(host="localhost", port=6333)

COLLECTION_NAME = "documents_chunks"

# Sample chunks (small & safe test)
sample_chunks = [
    "Enterprise search systems use vector databases for semantic retrieval.",
    "Retrieval Augmented Generation combines search with language models.",
    "Qdrant is a fast vector database designed for similarity search."
]

# Generate embeddings
embedding_service = EmbeddingService()
embeddings = embedding_service.embed_texts(sample_chunks)

# Prepare points
points = []
for idx, (text, vector) in enumerate(zip(sample_chunks, embeddings)):
    points.append(
        PointStruct(
            id=idx,
            vector=vector,
            payload={
                "text": text,
                "source": "sample_test"
            }
        )
    )

# Insert into Qdrant
client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)

print(f"Inserted {len(points)} vectors into '{COLLECTION_NAME}'")
