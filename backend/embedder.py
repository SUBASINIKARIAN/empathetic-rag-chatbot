from sentence_transformers import SentenceTransformer

_model = None


def get_embedder() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed(text: str) -> list[float]:
    return get_embedder().encode(text).tolist()


def embed_batch(texts: list[str]) -> list[list[float]]:
    return get_embedder().encode(texts).tolist()
