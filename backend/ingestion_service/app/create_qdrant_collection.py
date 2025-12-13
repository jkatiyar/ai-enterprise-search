from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

# Connect to local Qdrant
client = QdrantClient(
    host="localhost",
    port=6333
)

COLLECTION_NAME = "documents_chunks"

# Create collection
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=384,          # embedding size
        distance=Distance.COSINE
    )
)

print(f"Collection '{COLLECTION_NAME}' created successfully!")
