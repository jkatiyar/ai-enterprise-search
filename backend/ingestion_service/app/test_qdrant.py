from utils.qdrant_utils import get_qdrant_client

def test_qdrant():
    client = get_qdrant_client()
    collections = client.get_collections()
    print("Qdrant connected successfully!")
    print("Collections:", collections)

if __name__ == "__main__":
    test_qdrant()
