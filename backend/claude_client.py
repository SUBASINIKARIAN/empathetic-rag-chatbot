import os
import anthropic
from tone_detector import detect_tone, get_system_prompt
from query_rewriter import rewrite_query
from retriever import retrieve, build_context
from evaluator import evaluate_retrieval

_client = None


def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client


def chat(user_message: str, conversation_history: list[dict], session_id: str) -> dict:
    tone = detect_tone(user_message)

    rewritten = rewrite_query(user_message, conversation_history) if conversation_history else user_message

    chunks = retrieve(rewritten, top_k=5)
    context = build_context(chunks)
    avg_score = sum(c["score"] for c in chunks) / len(chunks) if chunks else 0.0

    system_prompt = get_system_prompt(tone)

    messages = conversation_history.copy()
    messages.append({
        "role": "user",
        "content": f"Context from knowledge base:\n{context}\n\nUser question: {user_message}",
    })

    response = get_client().messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system_prompt,
        messages=messages,
    )

    answer = response.content[0].text

    conversation_history.append({"role": "user", "content": user_message})
    conversation_history.append({"role": "assistant", "content": answer})

    eval_result = evaluate_retrieval(answer, chunks)

    return {
        "answer": answer,
        "retrieval_score": round(avg_score, 4),
        "tone_detected": tone,
        "grounding": eval_result,
        "sources": [c["text"][:120] + "..." for c in chunks[:2]],
    }
