from utils.embedding_utils import EmbeddingService

if __name__ == "__main__":
    service = EmbeddingService()

    sample_texts = [
        "Enterprise search systems use vector databases",
        "AI can understand documents semantically"
    ]

    embeddings = service.embed_texts(sample_texts)

    print("Number of embeddings:", len(embeddings))
    print("Embedding vector length:", len(embeddings[0]))
