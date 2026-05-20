from sklearn.metrics.pairwise import cosine_similarity
from embedder import embed


def evaluate_retrieval(answer: str, retrieved_chunks: list[dict]) -> dict:
    if not retrieved_chunks:
        return {"grounding_score": 0.0, "is_grounded": False, "hallucination_risk": "HIGH"}

    answer_embedding = embed(answer)
    chunk_embeddings = [embed(c["text"]) for c in retrieved_chunks]

    similarities = [
        cosine_similarity([answer_embedding], [ce])[0][0]
        for ce in chunk_embeddings
    ]
    max_similarity = float(max(similarities))

    return {
        "grounding_score": round(max_similarity, 4),
        "is_grounded": max_similarity > 0.65,
        "hallucination_risk": (
            "LOW" if max_similarity > 0.75
            else "MEDIUM" if max_similarity > 0.5
            else "HIGH"
        ),
    }
