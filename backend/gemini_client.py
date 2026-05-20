from google import genai
from google.genai import types
from key_manager import get_secret
from tone_detector import detect_tone, get_system_prompt
from query_rewriter import rewrite_query
from retriever import retrieve, build_context
from evaluator import evaluate_retrieval

MODEL = "gemini-flash-latest"
_client: genai.Client | None = None


def get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=get_secret("GEMINI_API_KEY"))
    return _client


def _build_history(conversation_history: list[dict]) -> list[types.Content]:
    history = []
    for msg in conversation_history:
        role = "model" if msg["role"] == "assistant" else "user"
        history.append(types.Content(role=role, parts=[types.Part(text=msg["content"])]))
    return history


def chat(user_message: str, conversation_history: list[dict], session_id: str) -> dict:
    tone = detect_tone(user_message)
    rewritten = rewrite_query(user_message, conversation_history) if conversation_history else user_message

    chunks = retrieve(rewritten, top_k=5)
    context = build_context(chunks)
    avg_score = sum(c["score"] for c in chunks) / len(chunks) if chunks else 0.0

    system_prompt = get_system_prompt(tone)
    history = _build_history(conversation_history)
    full_message = f"Context from knowledge base:\n{context}\n\nUser question: {user_message}"

    chat_session = get_client().chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
        history=history,
    )
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
