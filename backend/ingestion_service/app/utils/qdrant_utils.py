from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from core.qdrant_config import QDRANT_CONFIG

COLLECTION_NAME = "document_chunks"
VECTOR_SIZE = 384  # all-MiniLM-L6-v2

def get_qdrant_client():
    return QdrantClient(
        host=QDRANT_CONFIG["host"],
        port=QDRANT_CONFIG["port"]
    )

def create_collection_if_not_exists():
    client = get_qdrant_client()
    collections = client.get_collections().collections
    collection_names = [c.name for c in collections]

    if COLLECTION_NAME not in collection_names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE
            )
        )
        print(f"Collection '{COLLECTION_NAME}' created.")
    else:
        print(f"Collection '{COLLECTION_NAME}' already exists.")
