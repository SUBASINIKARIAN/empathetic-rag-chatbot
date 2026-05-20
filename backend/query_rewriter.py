import google.generativeai as genai
from key_manager import get_secret

_model = None


def get_model():
    global _model
    if _model is None:
        genai.configure(api_key=get_secret("GEMINI_API_KEY"))
        _model = genai.GenerativeModel("gemini-1.5-flash")
    return _model


def rewrite_query(original_query: str, conversation_history: list[dict]) -> str:
    history_text = "\n".join(
        f"{m['role']}: {m['content']}" for m in conversation_history[-4:]
    )
    prompt = (
        f"Given this conversation history:\n{history_text}\n\n"
        f"Rewrite the user's latest query to be more specific and self-contained "
        f"for document search:\nQuery: {original_query}\n\nRewritten query:"
    )
    response = get_model().generate_content(prompt)
    return response.text.strip()
