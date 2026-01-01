from qdrant_client import QdrantClient

client = QdrantClient(host="localhost", port=6333)

collections = client.get_collections().collections

for col in collections:
    print(f"Deleting collection: {col.name}")
    client.delete_collection(col.name)

print("✅ All Qdrant collections deleted")
