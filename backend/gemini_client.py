import google.generativeai as genai
from key_manager import get_secret
from tone_detector import detect_tone, get_system_prompt
from query_rewriter import rewrite_query
from retriever import retrieve, build_context
from evaluator import evaluate_retrieval

_model_cache: dict = {}


def get_model(tone: str):
    if tone not in _model_cache:
        genai.configure(api_key=get_secret("GEMINI_API_KEY"))
        _model_cache[tone] = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=get_system_prompt(tone),
        )
    return _model_cache[tone]


def _to_gemini_history(conversation_history: list[dict]) -> list[dict]:
    """Convert internal history format to Gemini's role/parts format."""
    gemini_history = []
    for msg in conversation_history:
        role = "model" if msg["role"] == "assistant" else "user"
        gemini_history.append({"role": role, "parts": [{"text": msg["content"]}]})
    return gemini_history


def chat(user_message: str, conversation_history: list[dict], session_id: str) -> dict:
    tone = detect_tone(user_message)

    rewritten = rewrite_query(user_message, conversation_history) if conversation_history else user_message

    chunks = retrieve(rewritten, top_k=5)
    context = build_context(chunks)
    avg_score = sum(c["score"] for c in chunks) / len(chunks) if chunks else 0.0

    model = get_model(tone)
    gemini_history = _to_gemini_history(conversation_history)
    chat_session = model.start_chat(history=gemini_history)

    full_message = f"Context from knowledge base:\n{context}\n\nUser question: {user_message}"
    response = chat_session.send_message(full_message)
    answer = response.text

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
