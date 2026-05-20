import os
from pinecone import Pinecone
from embedder import embed

_index = None


def get_index():
    global _index
    if _index is None:
        pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        _index = pc.Index(os.environ.get("PINECONE_INDEX_NAME", "empathetic-chatbot"))
    return _index


def retrieve(query: str, top_k: int = 5) -> list[dict]:
    query_embedding = embed(query)
    results = get_index().query(
        vector=query_embedding, top_k=top_k, include_metadata=True
    )
    return [
        {
            "text": r["metadata"].get("text", ""),
            "score": r["score"],
            "title": r["metadata"].get("title", ""),
        }
        for r in results["matches"]
    ]


def build_context(chunks: list[dict]) -> str:
    return "\n\n---\n\n".join(c["text"] for c in chunks)
