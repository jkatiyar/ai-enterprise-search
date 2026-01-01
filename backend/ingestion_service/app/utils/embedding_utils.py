from sentence_transformers import SentenceTransformer
from typing import List

MODEL_NAME = "all-MiniLM-L6-v2"

# Singleton model (important: load once)
_model = SentenceTransformer(MODEL_NAME)


def embed_query(text: str) -> List[float]:
    """
    Embed a single query string into a vector
    """
    embedding = _model.encode(
        text,
        convert_to_numpy=True
    )
    return embedding.tolist()


class EmbeddingService:
    """
    Used for bulk embeddings (PDF ingestion, chunking, etc.)
    """

    def __init__(self):
        self.model = _model

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True
        )
        return embeddings.tolist()
