from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True
        )
        return embeddings.tolist()
