from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

COLLECTION_NAME = "documents"
VECTOR_SIZE = 384  # all-MiniLM-L6-v2

client = QdrantClient(host="localhost", port=6333)

collections = client.get_collections().collections
existing_names = [c.name for c in collections]

if COLLECTION_NAME in existing_names:
    print(f"Collection '{COLLECTION_NAME}' already exists")
else:
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE,
        ),
    )
    print(f"Collection '{COLLECTION_NAME}' created successfully")
